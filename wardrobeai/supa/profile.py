from datetime import datetime, timedelta, timezone
import re
from typing import Optional, Dict, Any, List
from .client import supabase

# NOTE:
# All operations below use Supabase tables protected by RLS policies.
# We authenticate PostgREST with the user's access token so policies enforce per-user access.
# Expected tables (with RLS and policies):
# - profiles(user_id PK/unique)
# - subscriptions(user_id, status, expires_at, created_at)
# - usage_tracking(user_id, feature, count, date, created_at)

def _with_user(token: str):
    """Attach user JWT to PostgREST so RLS policies are enforced."""
    if not token:
        raise ValueError("Missing Supabase auth token")
    supabase.postgrest.auth(token)
    return supabase

# -----------------------
# Profile Management
# -----------------------
def get_user_profile(email: str, token: str) -> Optional[Dict[str, Any]]:
    """Fetch the user's profile row via RLS."""
    sb = _with_user(token)
    try:
        res = sb.table('profiles').select('*').eq('email', email).limit(1).execute()
        rows = res.data or []
        return rows[0] if rows else None
    except Exception as e:
        print(f"get_user_profile error: {e}")
        return None

def update_user_profile(email: str, profile_data: Dict[str, Any], token: str) -> Dict[str, Any]:
    """Upsert the user's profile via RLS."""
    sb = _with_user(token)
    try:
        now = datetime.now(timezone.utc).isoformat()
        payload = {k: v for k, v in profile_data.items() if v is not None and v != ''}
        payload['updated_at'] = now

        # Check if exists
        existing = get_user_profile(email, token)
        if existing:
            res = sb.table('profiles').update(payload).eq('email', email).execute()
        else:
            payload['email'] = email
            payload['created_at'] = now
            res = sb.table('profiles').insert(payload).execute()

        data = (res.data or [])
        return {'success': True, 'data': data[0] if data else payload}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# -----------------------
# Subscription Management
# -----------------------
def get_user_subscription(email: str, token: str) -> Optional[Dict[str, Any]]:
    """Return latest active subscription if any."""
    sb = _with_user(token)
    try:
        res = (
            sb.table('subscriptions')
            .select('*')
            .eq('email', email)
            .eq('status', 'active')
            .order('created_at', desc=True)
            .limit(1)
            .execute()
        )
        rows = res.data or []
        print(f"DEBUG get_user_subscription for email {email}: found {len(rows)} active subs, first: {rows[0] if rows else None}")
        return rows[0] if rows else None
    except Exception as e:
        print(f"get_user_subscription error: {e}")
        return None

def _expire_subscription(email: str, subscription_id: str, token: str) -> None:
    """Mark a subscription as expired via RLS."""
    sb = _with_user(token)
    try:
        sb.table('subscriptions').update({'status': 'expired'}).eq('id', subscription_id).execute()
    except Exception as e:
        print(f"_expire_subscription error: {e}")

def create_subscription(email: str, plan_type: str, token: str, payment_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a new active subscription and expire existing active ones."""
    sb = _with_user(token)
    try:
        # Expire any current active subs
        try:
            active_res = (
                sb.table('subscriptions')
                .select('id,status')
                .eq('email', email)
                .eq('status', 'active')
                .execute()
            )
            for row in (active_res.data or []):
                if row.get('status') == 'active':
                    sb.table('subscriptions').update({'status': 'expired'}).eq('id', row['id']).execute()
        except Exception as e:
            # Don't fail whole flow if cleanup fails
            print(f"create_subscription cleanup error: {e}")

        now = datetime.now(timezone.utc)
        subscription = {
            'email': email,
            'plan_type': plan_type,
            'status': 'active',
            'payment_id': payment_id,
            'started_at': now.isoformat(),
            'expires_at': (now + timedelta(days=30)).isoformat(),  # monthly by default
            'created_at': now.isoformat(),
        }

        res = sb.table('subscriptions').insert(subscription).execute()
        data = (res.data or [])
        return {'success': True, 'data': data[0] if data else subscription}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def check_subscription_status(email: str, token: str) -> bool:
    """Return True if user has a non-expired active subscription."""
    try:
        sub = get_user_subscription(email, token)
        if not sub:
            print(f"DEBUG check_subscription_status for {email}: no active sub")
            return False
        # Expiration check
        expires_at = sub.get('expires_at')
        if not expires_at:
            print(f"DEBUG check_subscription_status for {email}: active sub with no expires_at")
            return True
        exp_dt_str = expires_at.replace('Z', '+00:00')
        # Remove microseconds if present before timezone offset
        exp_dt_str = re.sub(r'\.\d+(?=[+-])', '', exp_dt_str)
        if len(exp_dt_str) == 19:
            exp_dt_str += '+00:00'
        exp_dt = datetime.fromisoformat(exp_dt_str)
        now = datetime.now(timezone.utc)
        print(f"DEBUG check_subscription_status for {email}: expires_at '{expires_at}' -> {exp_dt}, now {now}, expired: {now > exp_dt}")
        if now > exp_dt:
            _expire_subscription(email, sub.get('id'), token)
            return False
        return True
    except Exception as e:
        print(f"check_subscription_status error: {e}")
        return False

# -----------------------
# Usage Tracking and Access Policies
# -----------------------
def track_usage(email: str, feature: str, token: str, count: int = 1) -> Dict[str, Any]:
    """Insert a usage record (RLS will ensure only own rows)."""
    sb = _with_user(token)
    try:
        row = {
            'email': email,
            'feature': feature,
            'count': count,
            'date': datetime.now(timezone.utc).date().isoformat(),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        sb.table('usage_tracking').insert(row).execute()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_daily_usage(email: str, feature: str, token: str) -> int:
    """Sum today's usage count for a feature."""
    sb = _with_user(token)
    try:
        today = datetime.now(timezone.utc).date().isoformat()
        res = (
            sb.table('usage_tracking')
            .select('count')
            .eq('email', email)
            .eq('feature', feature)
            .eq('date', today)
            .execute()
        )
        rows = res.data or []
        return sum(int(r.get('count', 0)) for r in rows)
    except Exception as e:
        print(f"get_daily_usage error: {e}")
        return 0

def get_free_limits() -> Dict[str, int]:
    """Define usage limits for free users."""
    return {
        'daily_generations': 1,
        'daily_suggestions': 1,
        'monthly_generations': 5,
    }

def check_feature_access(email: str, feature: str, token: str) -> bool:
    """Policy: premium users have access; free users are limited by daily quotas."""
    if check_subscription_status(email, token):
        return True
    limits = get_free_limits()
    limit = limits.get('daily_generations' if feature == 'generations' else feature, 0)
    used = get_daily_usage(email, feature, token)
    return used < limit

# -----------------------
# Dashboard Stats and Activity
# -----------------------
def get_wardrobe_stats(email: str, token: str) -> Dict[str, Any]:
    """Fetch user stats for dashboard: item count, generations, planned, recent activity."""
    sb = _with_user(token)
    try:
        # Total wardrobe items
        items_res = sb.table('wardrobe_items').select('count', count='exact').eq('email', email).execute()
        item_count = items_res.count or 0

        # Total generated outfits
        generations_res = sb.table('generated_outfits').select('count', count='exact').eq('email', email).execute()
        generations_count = generations_res.count or 0

        # Planned outfits this week (last 7 days)
        from datetime import datetime, timedelta
        week_start = (datetime.now(timezone.utc) - timedelta(days=7)).date().isoformat()
        planned_res = (
            sb.table('planned_outfits')
            .select('count', count='exact')
            .eq('email', email)
            .gte('created_at', week_start)
            .execute()
        )
        planned_count = planned_res.count or 0

        # Recent activity (last 7 days, limited to 3)
        activity_res = (
            sb.table('user_activity')
            .select('*')
            .eq('email', email)
            .order('timestamp', desc=True)
            .lte('timestamp', datetime.now(timezone.utc).isoformat())
            .gte('timestamp', week_start)
            .limit(3)
            .execute()
        )
        recent_activity = activity_res.data or []

        return {
            'item_count': item_count,
            'generations_count': generations_count,
            'planned_count': planned_count,
            'recent_activity': recent_activity
        }
    except Exception as e:
        print(f"get_wardrobe_stats error for {email}: {e}")
        return {'item_count': 0, 'generations_count': 0, 'planned_count': 0, 'recent_activity': []}

def track_wardrobe_action(email: str, token: str, action: str, details: Optional[str] = None) -> bool:
    """Log user activity to user_activity table."""
    sb = _with_user(token)
    try:
        activity = {
            'email': email,
            'action': action,
            'details': details,
        }
        sb.table('user_activity').insert(activity).execute()
        return True
    except Exception as e:
        print(f"track_wardrobe_action error for {email}: {e}")
        return False

def add_wardrobe_item(email: str, token: str, name: str, category: str, color: Optional[str] = None, size: Optional[str] = None) -> bool:
    """Add a new item to wardrobe_items."""
    sb = _with_user(token)
    try:
        item = {
            'email': email,
            'name': name,
            'category': category,
            'color': color,
            'size': size,
        }
        sb.table('wardrobe_items').insert(item).execute()
        track_wardrobe_action(email, token, 'added_item', f'Added {name} ({category})')
        return True
    except Exception as e:
        print(f"add_wardrobe_item error for {email}: {e}")
        return False

def log_generated_outfit(email: str, token: str, prompt: str, style: str) -> bool:
    """Log AI generation to generated_outfits."""
    sb = _with_user(token)
    try:
        outfit = {
            'email': email,
            'prompt': prompt,
            'style': style,
        }
        sb.table('generated_outfits').insert(outfit).execute()
        track_wardrobe_action(email, token, 'generated_outfit', f'Generated outfit: {prompt[:50]}...')
        return True
    except Exception as e:
        print(f"log_generated_outfit error for {email}: {e}")
        return False

def log_planned_outfit(email: str, token: str, description: str, planned_date: str) -> bool:
    """Log planned outfit to planned_outfits."""
    sb = _with_user(token)
    try:
        plan = {
            'email': email,
            'outfit_description': description,
            'planned_date': planned_date,
        }
        sb.table('planned_outfits').insert(plan).execute()
        track_wardrobe_action(email, token, 'planned_outfit', f'Planned: {description[:50]}...')
        return True
    except Exception as e:
        print(f"log_planned_outfit error for {email}: {e}")
        return False

# -----------------------
# Favourites Management
# -----------------------
def add_favourite(email: str, token: str, outfit_type: str, outfit_description: str, image_url: Optional[str] = None, source_id: Optional[str] = None) -> bool:
    """Add a favourite outfit."""
    sb = _with_user(token)
    try:
        favourite = {
            'email': email,
            'outfit_type': outfit_type,
            'outfit_description': outfit_description,
            'image_url': image_url,
            'source_id': source_id,
        }
        sb.table('favourites').insert(favourite).execute()
        track_wardrobe_action(email, token, 'added_favourite', f'Added favourite: {outfit_description[:50]}...')
        return True
    except Exception as e:
        print(f"add_favourite error for {email}: {e}")
        return False

def get_favourites(email: str, token: str) -> List[Dict[str, Any]]:
    """Get user's favourite outfits."""
    sb = _with_user(token)
    try:
        res = sb.table('favourites').select('*').eq('email', email).order('created_at', desc=True).execute()
        return res.data or []
    except Exception as e:
        print(f"get_favourites error for {email}: {e}")
        return []

def remove_favourite(email: str, token: str, favourite_id: str) -> bool:
    """Remove a favourite outfit."""
    sb = _with_user(token)
    try:
        sb.table('favourites').delete().eq('id', favourite_id).eq('email', email).execute()
        track_wardrobe_action(email, token, 'removed_favourite', f'Removed favourite {favourite_id}')
        return True
    except Exception as e:
        print(f"remove_favourite error for {email}: {e}")
        return False