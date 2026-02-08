"""API routes for credits management."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.supabase import supabase_service
from middleware.auth import require_auth, AuthenticatedUser

router = APIRouter(prefix="/api/credits", tags=["credits"])


class CreditsResponse(BaseModel):
    credits_remaining: int
    credits_used_this_month: int
    tier: str
    tier_limit: int
    credits_reset_at: str | None = None


class UseCreditsResponse(BaseModel):
    success: bool
    credits_remaining: int
    message: str


@router.get("", response_model=CreditsResponse)
async def get_credits(user: AuthenticatedUser = Depends(require_auth)):
    """Get current user's credit information."""
    credits = await supabase_service.get_user_credits(user.id)
    return CreditsResponse(**credits)


@router.post("/use", response_model=UseCreditsResponse)
async def use_credit(user: AuthenticatedUser = Depends(require_auth)):
    """
    Use one credit for an analysis.
    Returns success status and remaining credits.
    """
    success = await supabase_service.use_credit(user.id)
    
    if not success:
        credits = await supabase_service.get_user_credits(user.id)
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "message": "No credits remaining. Please upgrade your plan or purchase credits.",
                "credits_remaining": credits["credits_remaining"],
                "tier": credits["tier"]
            }
        )
    
    # Get updated credits
    credits = await supabase_service.get_user_credits(user.id)
    return UseCreditsResponse(
        success=True,
        credits_remaining=credits["credits_remaining"],
        message="Credit used successfully"
    )


@router.get("/check")
async def check_credits(user: AuthenticatedUser = Depends(require_auth)):
    """Check if user has credits available (pre-analysis check)."""
    credits = await supabase_service.get_user_credits(user.id)
    has_credits = credits["credits_remaining"] > 0
    
    return {
        "has_credits": has_credits,
        "credits_remaining": credits["credits_remaining"],
        "tier": credits["tier"],
        "tier_limit": credits["tier_limit"],
        "message": "Credits available" if has_credits else "No credits remaining"
    }
