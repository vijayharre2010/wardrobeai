# Supabase RLS Policies for WardrobeAI

## Overview

This document outlines the Row Level Security (RLS) policies implemented in the WardrobeAI Supabase database. All tables have RLS enabled, and policies are designed to ensure users can only access, insert, or update their own data. Access is enforced using the user's email extracted from the JWT token (`auth.jwt() ->> 'email'`). The schema uses `email` as the primary identifier (TEXT NOT NULL UNIQUE) instead of UUID user_id.

Policies are defined in `wardrobeai/supa/setup_tables.sql`.

## Profiles Table

The `profiles` table stores user-specific information like height, age, gender, etc.

- **Policy: Users can view their own profile**  
  `FOR SELECT USING (auth.jwt() ->> 'email' = email)`  
  Allows SELECT only on rows where the email matches the authenticated user's email.

- **Policy: Users can insert their own profile**  
  `FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email)`  
  Allows INSERT only if the provided email matches the authenticated user's email.

- **Policy: Users can update their own profile**  
  `FOR UPDATE USING (auth.jwt() ->> 'email' = email)`  
  Allows UPDATE only on rows where the email matches the authenticated user's email.

## Subscriptions Table

The `subscriptions` table manages user subscription details, including plan type, status, and expiration.

- **Policy: Users can view their own subscriptions**  
  `FOR SELECT USING (auth.jwt() ->> 'email' = email)`  
  Allows SELECT only on rows where the email matches the authenticated user's email.

- **Policy: Users can insert their own subscriptions**  
  `FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email)`  
  Allows INSERT only if the provided email matches the authenticated user's email.

- **Policy: Users can update their own subscriptions**  
  `FOR UPDATE USING (auth.jwt() ->> 'email' = email)`  
  Allows UPDATE only on rows where the email matches the authenticated user's email.

## Usage Tracking Table

The `usage_tracking` table logs feature usage for rate limiting and quotas.

- **Policy: Users can view their own usage**  
  `FOR SELECT USING (auth.jwt() ->> 'email' = email)`  
  Allows SELECT only on rows where the email matches the authenticated user's email.

- **Policy: Users can insert their own usage**  
  `FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email)`  
  Allows INSERT only if the provided email matches the authenticated user's email.

## Additional Notes

- **Authentication**: All operations authenticate via the user's JWT token using Supabase's PostgREST client. The `_with_user(token)` helper attaches the token for RLS enforcement.
- **Cascade Deletes**: Subscriptions and usage_tracking reference profiles.email with ON DELETE CASCADE.
- **Indexes**: Indexes on `email` fields improve query performance for user-specific lookups.
- **Triggers**: An `update_updated_at_column` trigger automatically updates `updated_at` on profiles modifications.

To apply these policies, run `setup_tables.sql` in the Supabase SQL Editor. Ensure RLS is enabled on all tables.