# Policy-Based User Management for WardrobeAI

This folder contains the policy-based user management system for the WardrobeAI application. Instead of using a traditional database, this system uses configurable policies and file-based storage to manage user profiles, subscriptions, and feature access.

## Files

- `client.py` - Supabase client configuration (for authentication only)
- `auth.py` - Authentication functions using Supabase
- `profile.py` - Policy-based profile and subscription management
- `setup_tables.sql` - Legacy SQL script (no longer needed)
- `__init__.py` - Package initialization

## Architecture

The system uses a **policy-based approach** where:

1. **User data** is stored in JSON files (`wardrobeai/data/user_{user_id}.json`)
2. **Policies** define feature access rules and limits
3. **Business logic** determines user status based on policies rather than stored data
4. **File-based storage** provides persistence without requiring a database

## Setup

1. **No Database Required**: The system works out-of-the-box with file storage
2. **Configure Policies**: Modify policy functions in `profile.py` to change behavior
3. **Data Directory**: User data is automatically stored in `wardrobeai/data/`

## Policy Definitions

### Premium Features Policy
```python
def get_premium_features():
    return {
        'unlimited_generations': True,
        'priority_processing': True,
        'premium_styles': True,
        'advanced_filters': True
    }
```

### Free User Limits Policy
```python
def get_free_limits():
    return {
        'daily_generations': 1,
        'daily_suggestions': 1,
        'monthly_generations': 5
    }
```

## Key Functions

### Profile Management
- `get_user_profile(user_id)` - Retrieve user profile from file storage
- `update_user_profile(user_id, profile_data)` - Save/update profile to file

### Policy-Based Subscription Management
- `check_subscription_status(user_id)` - Check if user has active premium (policy-based)
- `create_subscription(user_id, plan_type)` - Create new subscription (file-based)
- `get_user_subscription(user_id)` - Get current subscription from file

### Usage Tracking & Access Control
- `track_usage(user_id, feature)` - Track feature usage in files
- `get_daily_usage(user_id, feature)` - Get today's usage count
- `check_feature_access(user_id, feature)` - Check if user can access feature based on policies

## Data Storage Structure

User data is stored in JSON format:
```json
{
  "profile": {
    "height": "170",
    "age": "25",
    "gender": "male",
    "style_preference": "casual"
  },
  "subscriptions": [
    {
      "id": "user123_1640995200",
      "plan_type": "premium",
      "status": "active",
      "started_at": "2023-01-01T00:00:00",
      "expires_at": "2023-02-01T00:00:00"
    }
  ],
  "usage": {
    "daily_suggestions": {
      "2023-01-01": 1
    },
    "generations": {
      "2023-01-01": 2
    }
  }
}
```

## Advantages of Policy-Based Approach

1. **No Database Dependency**: Works without external database setup
2. **Configurable Policies**: Easy to modify business rules
3. **File-Based Storage**: Simple persistence mechanism
4. **Policy-Driven Logic**: Business rules are explicit and testable
5. **Easy Migration**: Can be easily converted to database storage later

## Integration

The policy-based system is integrated into the Flask app in `app.py`:

- Profile updates are saved to JSON files
- Subscription status is determined by policy evaluation
- Usage limits are enforced based on configurable policies
- Feature access is controlled by policy functions