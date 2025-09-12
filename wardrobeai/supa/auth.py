import os
from .client import supabase

def send_magic_link(email: str, redirect_to: str) -> dict:
    """Send a Supabase magic link email, redirecting back to given URL."""
    try:
        # Prefer new SDK signature: options.email_redirect_to
        payload = {
            'email': email,
            'should_create_user': True,
            'options': {
                'email_redirect_to': redirect_to
            }
        }
        try:
            supabase.auth.sign_in_with_otp(payload)
        except TypeError:
            # Fallback: older SDK may accept top-level email_redirect_to
            supabase.auth.sign_in_with_otp({
                'email': email,
                'should_create_user': True,
                'email_redirect_to': redirect_to
            })
        return {'status': 'ok', 'message': 'Magic link sent'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def send_email_otp(email: str) -> dict:
    """Send email OTP for verification."""
    try:
        # Prefer explicit OTP (numeric code) by setting type='email'.
        # Some SDK versions may not accept 'type'; fall back gracefully.
        payload = {
            'email': email,
            'should_create_user': True,
            'type': 'email'
        }
        try:
            supabase.auth.sign_in_with_otp(payload)
        except TypeError:
            # Older SDKs without 'type' support
            supabase.auth.sign_in_with_otp({
                'email': email,
                'should_create_user': True
            })
        return {'status': 'ok', 'message': 'OTP sent'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def verify_email_otp(email: str, token: str) -> tuple:
    """Verify email OTP and return session token."""
    try:
        res = supabase.auth.verify_otp({
            'email': email,
            'token': token,
            'type': 'email'
        })
        if res.session:
            return (True, res.session.access_token, None)
        else:
            return (False, None, 'No session returned')
    except Exception as e:
        return (False, None, str(e))

def set_session_cookie(resp, token: str) -> None:
    """Set secure session cookie with appropriate flags."""
    # Determine secure flag based on environment
    cookie_secure = os.environ.get('COOKIE_SECURE', 'auto').lower()
    
    if cookie_secure == 'true':
        secure = True
    elif cookie_secure == 'false':
        secure = False
    else:  # auto
        env = os.environ.get('FLASK_ENV', '') or os.environ.get('APP_ENV', '')
        secure = env.lower() in ('production', 'prod')
    
    # Set cookie with security flags
    resp.set_cookie(
        'supabase_session',
        token,
        httponly=True,
        samesite='Lax',
        secure=secure,
        path='/',
        max_age=60*60*24*7  # 1 week
    )

def get_user_from_session(token: str):
    """Get user from session token."""
    if not token:
        return None
    
    try:
        user = supabase.auth.get_user(token)
        return user
    except Exception:
        return None
