"""Polar.sh integration for metered billing and usage tracking."""
import os
import httpx
import hmac
import hashlib
from typing import Optional


class PolarService:
    """Service for Polar.sh metered billing operations."""
    
    def __init__(self):
        self.api_key = os.getenv("POLAR_API_KEY")
        self.webhook_secret = os.getenv("POLAR_WEBHOOK_SECRET")
        self.base_url = "https://api.polar.sh/v1"
        self.meter_slug = "resume-analyses"  # Your meter name in Polar
    
    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    # =========================================
    # Meter Events (Usage Tracking)
    # =========================================
    
    async def record_usage(self, customer_id: str, quantity: int = 1) -> bool:
        """
        Record a meter event for analysis usage.
        
        This tells Polar that the customer used X credits.
        Polar handles the enforcement (checking limits, etc.)
        
        Args:
            customer_id: Polar customer ID
            quantity: Number of analyses to record (usually 1)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.api_key:
            print("POLAR_API_KEY not set, skipping usage tracking")
            return True  # Allow in dev mode
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/meters/{self.meter_slug}/events",
                    headers=self.headers,
                    json={
                        "customer_id": customer_id,
                        "value": quantity
                    }
                )
                return response.status_code in (200, 201, 202)
            except Exception as e:
                print(f"Failed to record Polar usage: {e}")
                return False
    
    async def get_customer_usage(self, customer_id: str) -> dict:
        """
        Get current usage for a customer.
        
        Returns meter balance (used, remaining, limit).
        """
        if not self.api_key:
            return {"used": 0, "remaining": 999, "limit": 999}  # Dev mode
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/customers/{customer_id}/meters/{self.meter_slug}",
                    headers=self.headers
                )
                if response.status_code == 200:
                    return response.json()
                return {"used": 0, "remaining": 0, "limit": 0}
            except Exception as e:
                print(f"Failed to get Polar usage: {e}")
                return {"used": 0, "remaining": 0, "limit": 0}
    
    async def check_can_analyze(self, customer_id: str) -> tuple[bool, int]:
        """
        Check if customer can perform an analysis.
        
        Returns:
            Tuple of (can_analyze, remaining_credits)
        """
        usage = await self.get_customer_usage(customer_id)
        remaining = usage.get("remaining", 0)
        return remaining > 0, remaining
    
    # =========================================
    # Customer Operations
    # =========================================
    
    async def create_customer(self, email: str, name: str = "") -> Optional[str]:
        """
        Create a new customer in Polar.
        
        Returns the customer ID.
        """
        if not self.api_key:
            return f"dev_customer_{email}"  # Dev mode
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/customers",
                    headers=self.headers,
                    json={
                        "email": email,
                        "name": name or email.split("@")[0]
                    }
                )
                if response.status_code in (200, 201):
                    return response.json().get("id")
                return None
            except Exception as e:
                print(f"Failed to create Polar customer: {e}")
                return None
    
    async def get_customer(self, customer_id: str) -> Optional[dict]:
        """Get customer details from Polar."""
        if not self.api_key:
            return {"id": customer_id, "email": "dev@example.com"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/customers/{customer_id}",
                    headers=self.headers
                )
                if response.status_code == 200:
                    return response.json()
                return None
            except Exception as e:
                print(f"Failed to get Polar customer: {e}")
                return None
    
    # =========================================
    # Webhook Verification
    # =========================================
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify Polar webhook signature.
        
        Args:
            payload: Raw request body
            signature: X-Polar-Signature header value
            
        Returns:
            True if signature is valid
        """
        if not self.webhook_secret:
            return True  # Allow in dev mode
        
        expected = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected}", signature)


# Singleton instance
polar_service = PolarService()
