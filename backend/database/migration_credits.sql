-- ============================================================
-- CREDITS SYSTEM MIGRATION
-- Run this in Supabase SQL Editor to add credits tracking
-- ============================================================

-- Add credits columns to profiles table
ALTER TABLE profiles 
ADD COLUMN IF NOT EXISTS credits_remaining INTEGER DEFAULT 3,
ADD COLUMN IF NOT EXISTS credits_used_this_month INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS credits_reset_at TIMESTAMPTZ DEFAULT NOW();

-- Set default credits based on tier
-- Free: 3, Pro: 30, Team: 100
UPDATE profiles 
SET credits_remaining = CASE 
    WHEN tier = 'free' THEN 3
    WHEN tier = 'pro' THEN 30
    WHEN tier = 'team' THEN 100
    ELSE 3
END
WHERE credits_remaining IS NULL;

-- ============================================================
-- FUNCTION: Get monthly credit limit by tier
-- ============================================================
CREATE OR REPLACE FUNCTION get_tier_credit_limit(user_tier TEXT)
RETURNS INTEGER AS $$
BEGIN
    RETURN CASE 
        WHEN user_tier = 'free' THEN 3
        WHEN user_tier = 'pro' THEN 30
        WHEN user_tier = 'team' THEN 100
        ELSE 3
    END;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- FUNCTION: Reset monthly credits (call from scheduled job)
-- ============================================================
CREATE OR REPLACE FUNCTION reset_monthly_credits()
RETURNS void AS $$
BEGIN
    UPDATE profiles
    SET 
        credits_remaining = get_tier_credit_limit(tier),
        credits_used_this_month = 0,
        credits_reset_at = NOW()
    WHERE credits_reset_at < NOW() - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- FUNCTION: Use a credit (called when analysis completes)
-- Returns: true if credit was deducted, false if insufficient
-- ============================================================
CREATE OR REPLACE FUNCTION use_credit(p_user_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    current_credits INTEGER;
BEGIN
    -- Get current credits
    SELECT credits_remaining INTO current_credits
    FROM profiles
    WHERE id = p_user_id;
    
    -- Check if user has credits
    IF current_credits IS NULL OR current_credits <= 0 THEN
        RETURN FALSE;
    END IF;
    
    -- Deduct credit
    UPDATE profiles
    SET 
        credits_remaining = credits_remaining - 1,
        credits_used_this_month = credits_used_this_month + 1
    WHERE id = p_user_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- FUNCTION: Add purchased credits
-- ============================================================
CREATE OR REPLACE FUNCTION add_credits(p_user_id UUID, p_amount INTEGER)
RETURNS void AS $$
BEGIN
    UPDATE profiles
    SET credits_remaining = credits_remaining + p_amount
    WHERE id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Grant execute permissions
GRANT EXECUTE ON FUNCTION get_tier_credit_limit(TEXT) TO authenticated;
GRANT EXECUTE ON FUNCTION use_credit(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION add_credits(UUID, INTEGER) TO service_role;
