"""Supabase client service for database and auth operations."""
import os
from supabase import create_client, Client
from functools import lru_cache


@lru_cache()
def get_supabase_client() -> Client:
    """Get singleton Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")  # Use service key for backend
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    
    return create_client(url, key)


class SupabaseService:
    """Service for Supabase database operations."""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    # =========================================
    # User/Profile Operations
    # =========================================
    
    async def get_profile(self, user_id: str) -> dict | None:
        """Get user profile by ID."""
        result = self.client.table("profiles").select("*").eq("id", user_id).single().execute()
        return result.data if result.data else None
    
    async def get_profile_by_polar_customer(self, polar_customer_id: str) -> dict | None:
        """Get user profile by Polar customer ID."""
        result = self.client.table("profiles").select("*").eq("polar_customer_id", polar_customer_id).single().execute()
        return result.data if result.data else None
    
    async def update_profile(self, user_id: str, **updates) -> dict:
        """Update user profile."""
        result = self.client.table("profiles").update(updates).eq("id", user_id).execute()
        return result.data[0] if result.data else {}
    
    async def set_polar_customer_id(self, user_id: str, polar_customer_id: str):
        """Link Polar customer ID to user profile."""
        await self.update_profile(user_id, polar_customer_id=polar_customer_id)
    
    async def update_tier(self, user_id: str, tier: str):
        """Update user's subscription tier."""
        await self.update_profile(user_id, tier=tier)
    
    # =========================================
    # Analysis Operations
    # =========================================
    
    async def create_analysis(
        self, 
        user_id: str, 
        job_title: str, 
        company_name: str, 
        company_url: str
    ) -> dict:
        """Create a new analysis record."""
        result = self.client.table("analyses").insert({
            "user_id": user_id,
            "job_title": job_title,
            "company_name": company_name,
            "company_url": company_url,
            "status": "completed"
        }).execute()
        return result.data[0] if result.data else {}
    
    async def get_user_analyses(self, user_id: str, limit: int = 50) -> list:
        """Get user's analysis history."""
        result = self.client.table("analyses").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
        return result.data or []
    
    async def get_analysis_count(self, user_id: str) -> int:
        """Get total number of analyses for a user."""
        result = self.client.table("analyses").select("id", count="exact").eq("user_id", user_id).execute()
        return result.count or 0
    
    # =========================================
    # Auth Verification
    # =========================================
    
    async def verify_jwt(self, token: str) -> dict | None:
        """Verify JWT and return user data."""
        try:
            # Use Supabase to verify the token
            user = self.client.auth.get_user(token)
            return user.user.model_dump() if user.user else None
        except Exception:
            return None


# Singleton instance
supabase_service = SupabaseService()
