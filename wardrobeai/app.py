from flask import Flask, request, redirect, url_for, render_template, jsonify, make_response, g, abort, render_template_string
import os, time, yaml
from datetime import datetime, timezone
from supa.auth import send_magic_link, set_session_cookie, get_user_from_session
from supa.profile import (
    update_user_profile as sp_update_user_profile,
    get_user_profile as sp_get_user_profile,
    check_subscription_status as sp_check_subscription_status,
    track_usage as sp_track_usage,
    get_daily_usage as sp_get_daily_usage,
    create_subscription as sp_create_subscription,
    check_feature_access as sp_check_feature_access,
    get_wardrobe_stats as sp_get_wardrobe_stats,
    log_generated_outfit as sp_log_generated_outfit,
    log_planned_outfit as sp_log_planned_outfit,
)
from ai.wardrobe_model import suggest_outfit, generate_outfit_images

# Load configuration
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# -----------------------
# App setup
# -----------------------
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-not-secure')

# Base URL for auth redirects (ensure this matches your Supabase Auth settings)
BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:8080')

# Simple in-memory rate limit for sending magic links:
# max 3 sends per 5 minutes per IP+email
RATE_LIMIT_WINDOW = 300  # seconds
RATE_LIMIT_MAX = 3
_RATE_BUCKET = {}

def _rate_limited(key: str):
    now = time.time()
    times = _RATE_BUCKET.get(key, [])
    times = [t for t in times if now - t < RATE_LIMIT_WINDOW]
    if len(times) >= RATE_LIMIT_MAX:
        _RATE_BUCKET[key] = times
        retry_after = int(RATE_LIMIT_WINDOW - (now - times[0]))
        return True, retry_after
    times.append(now)
    _RATE_BUCKET[key] = times
    return False, None

# -----------------------
# Current user resolution
# -----------------------
@app.before_request
def load_current_user():
    token = request.cookies.get('supabase_session')
    # Supabase SDK returns a UserResponse object from get_user(token)
    ur = get_user_from_session(token) if token else None
    g.current_user = ur
    g.session_token = token
    g.user_email = None
    try:
        if ur and getattr(ur, 'user', None):
            g.user_email = ur.user.email
    except Exception:
        g.user_email = None

# -----------------------
# Login required decorator
# -----------------------
def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if not getattr(g, 'user_email', None):
            return redirect(url_for('home'))
        return fn(*args, **kwargs)
    return decorated_function

# -----------------------
# Home page
# -----------------------
@app.route('/')
def home():
    return render_template('home.html', app_config=config)

# -----------------------
# Send OTP code
# -----------------------
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip().lower()
    if not email:
        return render_template('home.html', error='Email required', app_config=config)
    # Rate limit: key by IP + email
    key = f"{request.remote_addr}:{email}"
    limited, retry_after = _rate_limited(key)
    if limited:
        return render_template('home.html', error=f'Too many requests. Try again in {retry_after}s.', app_config=config)
    redirect_to = f"{BASE_URL}/auth/callback"
    res = send_magic_link(email, redirect_to)
    if res.get('status') == 'ok':
        return render_template('home.html', message='Magic link sent. Check your email.', app_config=config)
    else:
        return render_template('home.html', error=res.get('message', 'Failed to send magic link'), app_config=config)

# -----------------------
# Verify OTP code
# -----------------------
@app.route('/auth/callback')
def auth_callback():
    # Browser URL fragments (after '#') are never sent to the server.
    # Render a tiny page that reads the fragment and posts the token to the server.
    html = """
    <!doctype html>
    <html>
      <head><meta charset="utf-8"><title>Signing you in…</title></head>
      <body>
        <p>Signing you in…</p>
        <script>
        (function () {
          try {
            var hash = window.location.hash || '';
            var params = new URLSearchParams(hash.startsWith('#') ? hash.substring(1) : hash);
            var token = params.get('access_token') || params.get('accessToken') || params.get('token');
            if (!token) {
              document.body.innerHTML = '<p style="color:red">Missing access token in URL fragment.</p>';
              return;
            }
            fetch('/auth/finish', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              credentials: 'include',
              body: JSON.stringify({ token: token })
            })
            .then(function () { window.location.replace('/page/dashboard'); })
            .catch(function () { document.body.innerHTML = '<p style="color:red">Sign-in failed.</p>'; });
          } catch (e) {
            document.body.innerHTML = '<p style="color:red">Sign-in failed.</p>';
          }
        })();
        </script>
        <noscript>
          <p>Please enable JavaScript to complete sign-in.</p>
        </noscript>
      </body>
    </html>
    """
    return render_template_string(html)

@app.route('/auth/finish', methods=['POST'])
def auth_finish():
    token = (request.json or {}).get('token') if request.is_json else request.form.get('token')
    if not token:
        return ('Missing token', 400)
    resp = make_response('', 204)
    set_session_cookie(resp, token)
    return resp

@app.route('/logout', methods=['POST'])
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('supabase_session', path='/')
    return resp

# -----------------------
# API: get dynamic pages for navigation
# -----------------------
@app.route('/api/pages')
def get_pages():
    pages_dir = os.path.join(os.path.dirname(__file__), 'templates', 'pages')
    names = [os.path.splitext(f)[0] for f in os.listdir(pages_dir) if f.endswith('.html')]
    return jsonify({'pages': sorted(names)})

# -----------------------
# Protected dynamic page route
# -----------------------
@app.route('/page/<pagename>')
@login_required
def render_page(pagename):
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'pages', f'{pagename}.html')
    if not os.path.exists(template_path):
        abort(404)
    is_premium = sp_check_subscription_status(g.user_email, g.session_token)
    free_plan_message = config['messages']['free_plan_description'].format(limit=config['usage_limits']['daily_suggestions'])
    stats = None
    if pagename == 'dashboard':
        stats = sp_get_wardrobe_stats(g.user_email, g.session_token)
    return render_template('base.html', page=f'pages/{pagename}.html', is_premium=is_premium, free_plan_message=free_plan_message, stats=stats, app_config=config)

# -----------------------
# Daily outfit suggestions
# -----------------------
@app.route('/page/daily', methods=['GET', 'POST'])
@login_required
def daily_page():
    # Check feature access using Supabase RLS-backed policies
    is_premium = sp_check_subscription_status(g.user_email, g.session_token)
    has_access = sp_check_feature_access(g.user_email, 'daily_suggestions', g.session_token)
    usage_today = sp_get_daily_usage(g.user_email, 'daily_suggestions', g.session_token)

    daily_limit_message = config['messages']['daily_limit_description'].format(limit=config['usage_limits']['daily_suggestions'])
    if not has_access:
        return render_template('base.html', page='pages/daily.html',
                              limit_exceeded=True, is_premium=is_premium, daily_limit_message=daily_limit_message, app_config=config)

    outfit = None
    if request.method == 'POST':
        weather = request.form.get('weather', '')
        activity = request.form.get('activity', '')
        # Track usage
        sp_track_usage(g.user_email, 'daily_suggestions', g.session_token)
        # Generate suggestion
        outfit = suggest_outfit(weather, activity)
        # Log planned outfit
        if outfit:
            sp_log_planned_outfit(g.user_email, g.session_token, outfit, datetime.now(timezone.utc).date().isoformat())

    return render_template('base.html', page='pages/daily.html',
                          outfit=outfit, is_premium=is_premium, usage_today=usage_today, daily_limit_message=daily_limit_message, app_config=config)

# -----------------------
# AI outfit generator
# -----------------------
@app.route('/page/generate', methods=['GET', 'POST'])
@login_required
def generate_page():
    # Check feature access using Supabase RLS-backed policies
    is_premium = sp_check_subscription_status(g.user_email, g.session_token)
    has_access = sp_check_feature_access(g.user_email, 'generations', g.session_token)
    usage_today = sp_get_daily_usage(g.user_email, 'generations', g.session_token)

    generation_limit_message = config['messages']['generation_limit_description'].format(limit=config['usage_limits']['ai_generations'])
    if not has_access:
        return render_template('base.html', page='pages/generate.html',
                              limit_exceeded=True, is_premium=is_premium, generation_limit_message=generation_limit_message, app_config=config)

    generated_images = None
    prompt = ''
    style = ''
    if request.method == 'POST':
        prompt = request.form.get('prompt', '')
        style = request.form.get('style', '')
        # Track usage
        sp_track_usage(g.user_email, 'generations', g.session_token)
        # Generate images using gpt4free
        if prompt:
            generated_images = generate_outfit_images(prompt, style)
            # Log generated outfit
            sp_log_generated_outfit(g.user_email, g.session_token, prompt, style)

    image1_url = image2_url = image3_url = None
    if prompt and generated_images:
        if len(generated_images) > 0:
            image1_url = generated_images[0]
        if len(generated_images) > 1:
            image2_url = generated_images[1]
        if len(generated_images) > 2:
            image3_url = generated_images[2]

    return render_template('base.html', page='pages/generate.html',
                          image1_url=image1_url, image2_url=image2_url, image3_url=image3_url, is_premium=is_premium, usage_today=usage_today, generation_limit_message=generation_limit_message, app_config=config)

# -----------------------
# Helper functions removed to avoid name shadowing.
# All usage/limits/subscription checks are done via supa.profile functions with RLS.
# -----------------------

# -----------------------
# Profile page with personal details
# -----------------------
@app.route('/page/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    if request.method == 'POST':
        # Get form data
        profile_data = {
            'height': request.form.get('height'),
            'age': request.form.get('age'),
            'weight': request.form.get('weight'),
            'gender': request.form.get('gender'),
            'ethnicity': request.form.get('ethnicity'),
            'style_preference': request.form.get('style_preference'),
            'extra_info': request.form.get('extra_info')
        }

        # Save to Supabase (RLS enforced)
        result = sp_update_user_profile(g.user_email, profile_data, g.session_token)

        if result['success']:
            return render_template('base.html', page='pages/profile.html', profile_updated=True, app_config=config)
        else:
            return render_template('base.html', page='pages/profile.html', profile_error=result['error'], app_config=config)

    # Get existing profile data for GET request
    profile = sp_get_user_profile(g.user_email, g.session_token) if g.user_email else None
    is_premium = sp_check_subscription_status(g.user_email, g.session_token) if g.user_email else False
    return render_template('base.html', page='pages/profile.html', profile=profile, is_premium=is_premium, app_config=config)

# -----------------------
# Check subscription status (for popup)
# -----------------------
@app.route('/check_subscription')
@login_required
def check_subscription():
    is_premium = sp_check_subscription_status(g.user_email, g.session_token)
    return jsonify({'is_premium': is_premium})

# -----------------------
# Handle plan upgrades
# -----------------------
@app.route('/upgrade')
@login_required
def upgrade():
    plan_type = request.args.get('plan')
    if not plan_type:
        return redirect(url_for('render_page', pagename='profile'))

    # Simulate the upgrade; persistence handled by Supabase with RLS
    result = sp_create_subscription(g.user_email, plan_type, g.session_token)

    if result['success']:
        return redirect(url_for('render_page', pagename='profile'))
    else:
        profile = sp_get_user_profile(g.user_email, g.session_token) if g.user_email else None
        is_premium = sp_check_subscription_status(g.user_email, g.session_token) if g.user_email else False
        return render_template('base.html', page='pages/profile.html', profile=profile, is_premium=is_premium, upgrade_error=result['error'], app_config=config)

# -----------------------
# Error handlers
# -----------------------
@app.errorhandler(401)
def handle_unauthorized(e):
    return redirect(url_for('home'))

@app.errorhandler(404)
def handle_not_found(e):
    return ('Page not found', 404)

# -----------------------
# Run the app
# -----------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

