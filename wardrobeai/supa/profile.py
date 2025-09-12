from datetime import datetime, timedelta
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
def get_user_profile(user_id: str, token: str) -> Optional[Dict[str, Any]]:
    """Fetch the user's profile row via RLS."""
    sb = _with_user(token)
    try:
        res = sb.table('profiles').select('*').eq('user_id', user_id).limit(1).execute()
        rows = res.data or []
        return rows[0] if rows else None
    except Exception as e:
        print(f"get_user_profile error: {e}")
        return None

def update_user_profile(user_id: str, profile_data: Dict[str, Any], token: str) -> Dict[str, Any]:
    """Upsert the user's profile via RLS."""
    sb = _with_user(token)
    try:
        now = datetime.utcnow().isoformat()
        payload = {k: v for k, v in profile_data.items() if v is not None and v != ''}
        payload['updated_at'] = now

        # Check if exists
        existing = get_user_profile(user_id, token)
        if existing:
            res = sb.table('profiles').update(payload).eq('user_id', user_id).execute()
        else:
            payload['user_id'] = user_id
            payload['created_at'] = now
            res = sb.table('profiles').insert(payload).execute()

        data = (res.data or [])
        return {'success': True, 'data': data[0] if data else payload}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# -----------------------
# Subscription Management
# -----------------------
def get_user_subscription(user_id: str, token: str) -> Optional[Dict[str, Any]]:
    """Return latest active subscription if any."""
    sb = _with_user(token)
    try:
        res = (
            sb.table('subscriptions')
            .select('*')
            .eq('user_id', user_id)
            .eq('status', 'active')
            .order('created_at', desc=True)
            .limit(1)
            .execute()
        )
        rows = res.data or []
        return rows[0] if rows else None
    except Exception as e:
        print(f"get_user_subscription error: {e}")
        return None

def _expire_subscription(user_id: str, subscription_id: str, token: str) -> None:
    """Mark a subscription as expired via RLS."""
    sb = _with_user(token)
    try:
        sb.table('subscriptions').update({'status': 'expired'}).eq('id', subscription_id).execute()
    except Exception as e:
        print(f"_expire_subscription error: {e}")

def create_subscription(user_id: str, plan_type: str, token: str, payment_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a new active subscription and expire existing active ones."""
    sb = _with_user(token)
    try:
        # Expire any current active subs
        try:
            active_res = (
                sb.table('subscriptions')
                .select('id,status')
                .eq('user_id', user_id)
                .eq('status', 'active')
                .execute()
            )
            for row in (active_res.data or []):
                if row.get('status') == 'active':
                    sb.table('subscriptions').update({'status': 'expired'}).eq('id', row['id']).execute()
        except Exception as e:
            # Don't fail whole flow if cleanup fails
            print(f"create_subscription cleanup error: {e}")

        now = datetime.utcnow()
        subscription = {
            'user_id': user_id,
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

def check_subscription_status(user_id: str, token: str) -> bool:
    """Return True if user has a non-expired active subscription."""
    try:
        sub = get_user_subscription(user_id, token)
        if not sub:
            return False
        # Expiration check
        expires_at = sub.get('expires_at')
        if not expires_at:
            return True
        exp_dt = datetime.fromisoformat(expires_at.replace('Z', '+00:00')) if 'Z' in expires_at else datetime.fromisoformat(expires_at)
        if datetime.utcnow() > exp_dt:
            _expire_subscription(user_id, sub.get('id'), token)
            return False
        return True
    except Exception as e:
        print(f"check_subscription_status error: {e}")
        return False

# -----------------------
# Usage Tracking and Access Policies
# -----------------------
def track_usage(user_id: str, feature: str, token: str, count: int = 1) -> Dict[str, Any]:
    """Insert a usage record (RLS will ensure only own rows)."""
    sb = _with_user(token)
    try:
        row = {
            'user_id': user_id,
            'feature': feature,
            'count': count,
            'date': datetime.utcnow().date().isoformat(),
            'created_at': datetime.utcnow().isoformat(),
        }
        sb.table('usage_tracking').insert(row).execute()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_daily_usage(user_id: str, feature: str, token: str) -> int:
    """Sum today's usage count for a feature."""
    sb = _with_user(token)
    try:
        today = datetime.utcnow().date().isoformat()
        res = (
            sb.table('usage_tracking')
            .select('count')
            .eq('user_id', user_id)
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

def check_feature_access(user_id: str, feature: str, token: str) -> bool:
    """Policy: premium users have access; free users are limited by daily quotas."""
    if check_subscription_status(user_id, token):
        return True
    limits = get_free_limits()
    limit = limits.get('daily_generations' if feature == 'generations' else feature, 0)
    used = get_daily_usage(user_id, feature, token)
    return used < limit