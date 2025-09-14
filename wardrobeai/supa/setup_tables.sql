-- Supabase Tables Setup for WardrobeAI with RLS Policies
-- Run this SQL in your Supabase SQL Editor

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create profiles table
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    height TEXT,
    age TEXT,
    weight TEXT,
    gender TEXT,
    ethnicity TEXT,
    style_preference TEXT,
    extra_info TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create subscriptions table
CREATE TABLE IF NOT EXISTS public.subscriptions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email TEXT NOT NULL REFERENCES public.profiles(email) ON DELETE CASCADE,
    plan_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    payment_id TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create usage_tracking table
CREATE TABLE IF NOT EXISTS public.usage_tracking (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email TEXT NOT NULL REFERENCES public.profiles(email) ON DELETE CASCADE,
    feature TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 1,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create wardrobe_items table
CREATE TABLE IF NOT EXISTS public.wardrobe_items (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email TEXT NOT NULL REFERENCES public.profiles(email) ON DELETE CASCADE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    color TEXT,
    size TEXT,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create generated_outfits table
CREATE TABLE IF NOT EXISTS public.generated_outfits (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email TEXT NOT NULL REFERENCES public.profiles(email) ON DELETE CASCADE,
    prompt TEXT NOT NULL,
    style TEXT NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create planned_outfits table
CREATE TABLE IF NOT EXISTS public.planned_outfits (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email TEXT NOT NULL REFERENCES public.profiles(email) ON DELETE CASCADE,
    outfit_description TEXT NOT NULL,
    planned_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Create user_activity table
CREATE TABLE IF NOT EXISTS public.user_activity (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    email TEXT NOT NULL REFERENCES public.profiles(email) ON DELETE CASCADE,
    action TEXT NOT NULL,
    details TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- Enable RLS for new tables
ALTER TABLE public.wardrobe_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.generated_outfits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.planned_outfits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_activity ENABLE ROW LEVEL SECURITY;

-- RLS policies for wardrobe_items
CREATE POLICY "Users can view their own items" ON public.wardrobe_items FOR SELECT USING (auth.jwt() ->> 'email' = email);
CREATE POLICY "Users can insert their own items" ON public.wardrobe_items FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email);
CREATE POLICY "Users can update their own items" ON public.wardrobe_items FOR UPDATE USING (auth.jwt() ->> 'email' = email);
CREATE POLICY "Users can delete their own items" ON public.wardrobe_items FOR DELETE USING (auth.jwt() ->> 'email' = email);

-- RLS policies for generated_outfits
CREATE POLICY "Users can view their own generations" ON public.generated_outfits FOR SELECT USING (auth.jwt() ->> 'email' = email);
CREATE POLICY "Users can insert their own generations" ON public.generated_outfits FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email);

-- RLS policies for planned_outfits
CREATE POLICY "Users can view their own plans" ON public.planned_outfits FOR SELECT USING (auth.jwt() ->> 'email' = email);
CREATE POLICY "Users can insert their own plans" ON public.planned_outfits FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email);
CREATE POLICY "Users can update their own plans" ON public.planned_outfits FOR UPDATE USING (auth.jwt() ->> 'email' = email);
CREATE POLICY "Users can delete their own plans" ON public.planned_outfits FOR DELETE USING (auth.jwt() ->> 'email' = email);

-- RLS policies for user_activity
CREATE POLICY "Users can view their own activity" ON public.user_activity FOR SELECT USING (auth.jwt() ->> 'email' = email);
CREATE POLICY "Users can insert their own activity" ON public.user_activity FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email);

-- Enable Row Level Security
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.usage_tracking ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for profiles table
CREATE POLICY "Users can view their own profile" ON public.profiles
    FOR SELECT USING (auth.jwt() ->> 'email' = email);

CREATE POLICY "Users can insert their own profile" ON public.profiles
    FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email);

CREATE POLICY "Users can update their own profile" ON public.profiles
    FOR UPDATE USING (auth.jwt() ->> 'email' = email);

-- Create RLS policies for subscriptions table
CREATE POLICY "Users can view their own subscriptions" ON public.subscriptions
    FOR SELECT USING (auth.jwt() ->> 'email' = email);

CREATE POLICY "Users can insert their own subscriptions" ON public.subscriptions
    FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email);

CREATE POLICY "Users can update their own subscriptions" ON public.subscriptions
    FOR UPDATE USING (auth.jwt() ->> 'email' = email);

-- Create RLS policies for usage_tracking table
CREATE POLICY "Users can view their own usage" ON public.usage_tracking
    FOR SELECT USING (auth.jwt() ->> 'email' = email);

CREATE POLICY "Users can insert their own usage" ON public.usage_tracking
    FOR INSERT WITH CHECK (auth.jwt() ->> 'email' = email);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_profiles_email ON public.profiles(email);
CREATE INDEX IF NOT EXISTS idx_subscriptions_email ON public.subscriptions(email);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON public.subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_email ON public.usage_tracking(email);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_feature ON public.usage_tracking(feature);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_date ON public.usage_tracking(date);

CREATE INDEX IF NOT EXISTS idx_wardrobe_items_email ON public.wardrobe_items(email);
CREATE INDEX IF NOT EXISTS idx_generated_outfits_email ON public.generated_outfits(email);
CREATE INDEX IF NOT EXISTS idx_planned_outfits_email ON public.planned_outfits(email);
CREATE INDEX IF NOT EXISTS idx_planned_outfits_date ON public.planned_outfits(planned_date);
CREATE INDEX IF NOT EXISTS idx_user_activity_email ON public.user_activity(email);
CREATE INDEX IF NOT EXISTS idx_user_activity_timestamp ON public.user_activity(timestamp);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc'::text, NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for profiles table
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();