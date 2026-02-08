"""Polar.sh webhook handlers for subscription and payment events."""
from fastapi import APIRouter, Request, HTTPException
from services.polar import polar_service
from services.supabase import supabase_service


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/polar")
async def handle_polar_webhook(request: Request):
    """
    Handle Polar.sh webhook events.
    
    Events we care about:
    - subscription.created: User subscribed, update tier
    - subscription.updated: Plan changed
    - subscription.cancelled: User cancelled
    - checkout.completed: One-time purchase (credit pack)
    """
    # Get raw body for signature verification
    body = await request.body()
    signature = request.headers.get("X-Polar-Signature", "")
    
    # Verify webhook signature
    if not polar_service.verify_webhook_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    # Parse event
    event = await request.json()
    event_type = event.get("type", "")
    data = event.get("data", {})
    
    # Route to appropriate handler
    handlers = {
        "subscription.created": handle_subscription_created,
        "subscription.updated": handle_subscription_updated,
        "subscription.cancelled": handle_subscription_cancelled,
        "checkout.completed": handle_checkout_completed,
    }
    
    handler = handlers.get(event_type)
    if handler:
        await handler(data)
    
    return {"status": "ok"}


async def handle_subscription_created(data: dict):
    """Handle new subscription - update user tier."""
    customer_id = data.get("customer_id")
    product = data.get("product", {})
    product_name = product.get("name", "").lower()
    
    # Determine tier from product name
    tier = "free"
    if "pro" in product_name:
        tier = "pro"
    elif "team" in product_name:
        tier = "team"
    
    # Find user by Polar customer ID and update tier
    profile = await supabase_service.get_profile_by_polar_customer(customer_id)
    if profile:
        await supabase_service.update_tier(profile["id"], tier)
        print(f"Updated user {profile['id']} to tier: {tier}")


async def handle_subscription_updated(data: dict):
    """Handle subscription change (upgrade/downgrade)."""
    # Same logic as created - update tier based on new product
    await handle_subscription_created(data)


async def handle_subscription_cancelled(data: dict):
    """Handle subscription cancellation - revert to free tier."""
    customer_id = data.get("customer_id")
    
    profile = await supabase_service.get_profile_by_polar_customer(customer_id)
    if profile:
        await supabase_service.update_tier(profile["id"], "free")
        print(f"User {profile['id']} cancelled subscription, reverted to free")


async def handle_checkout_completed(data: dict):
    """
    Handle one-time purchase (credit pack).
    
    For metered billing, Polar handles the credit addition automatically.
    We just log the event here.
    """
    customer_id = data.get("customer_id")
    product = data.get("product", {})
    product_name = product.get("name", "")
    
    print(f"Credit pack purchased: {product_name} for customer {customer_id}")
    # Polar's meter system handles the credit addition automatically
