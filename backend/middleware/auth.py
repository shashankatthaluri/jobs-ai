"""Auth middleware for protecting API routes."""
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from services.supabase import supabase_service
from services.polar import polar_service


security = HTTPBearer(auto_error=False)


class AuthenticatedUser:
    """Authenticated user with profile data."""
    
    def __init__(
        self, 
        id: str, 
        email: str, 
        tier: str = "free",
        polar_customer_id: Optional[str] = None
    ):
        self.id = id
        self.email = email
        self.tier = tier
        self.polar_customer_id = polar_customer_id


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[AuthenticatedUser]:
    """
    Get current authenticated user from JWT token.
    
    Returns None if no valid auth (for optional auth routes).
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    user_data = await supabase_service.verify_jwt(token)
    
    if not user_data:
        return None
    
    # Get profile for additional data
    profile = await supabase_service.get_profile(user_data["id"])
    
    return AuthenticatedUser(
        id=user_data["id"],
        email=user_data.get("email", ""),
        tier=profile.get("tier", "free") if profile else "free",
        polar_customer_id=profile.get("polar_customer_id") if profile else None
    )


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> AuthenticatedUser:
    """
    Require authentication - raises 401 if not authenticated.
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    user = await get_current_user(credentials)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user


async def require_credits(
    user: AuthenticatedUser = Depends(require_auth)
) -> AuthenticatedUser:
    """
    Require authentication AND available credits.
    
    Checks Polar meter for credit availability.
    Raises 402 if no credits remaining.
    """
    # Free tier check (handled in app, 3/month)
    if user.tier == "free":
        # Get analysis count this month for free users
        from datetime import datetime
        analyses = await supabase_service.get_user_analyses(user.id, limit=100)
        
        # Count analyses this month
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        month_analyses = [
            a for a in analyses 
            if a.get("created_at") and a["created_at"] >= month_start.isoformat()
        ]
        
        if len(month_analyses) >= 3:
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "credit_exhausted",
                    "message": "Free tier limit reached (3/month). Upgrade to continue.",
                    "remaining": 0,
                    "tier": "free"
                }
            )
        
        return user
    
    # Paid tier - check Polar meter
    if not user.polar_customer_id:
        # No Polar customer ID yet - create one
        customer_id = await polar_service.create_customer(user.email)
        if customer_id:
            await supabase_service.set_polar_customer_id(user.id, customer_id)
            user.polar_customer_id = customer_id
    
    if user.polar_customer_id:
        can_analyze, remaining = await polar_service.check_can_analyze(user.polar_customer_id)
        
        if not can_analyze:
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "credit_exhausted",
                    "message": "No credits remaining. Purchase more to continue.",
                    "remaining": 0,
                    "tier": user.tier
                }
            )
    
    return user
