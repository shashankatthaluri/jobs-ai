"""LLM Service for JSON generation with rate limit handling."""
import json
import asyncio
import httpx
from typing import Any

from config import settings


MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds, will exponentially increase


class LLMService:
    """Async LLM client for structured JSON generation."""
    
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL
        self.model = settings.LLM_MODEL
    
    async def generate_json(
        self,
        user_prompt: str,
        system_prompt: str,
        temperature: float = 0.1
    ) -> dict[str, Any]:
        """
        Generate JSON response from LLM with retry logic for rate limits.
        
        Args:
            user_prompt: The user message content
            system_prompt: The system instruction
            temperature: Sampling temperature (lower = more deterministic)
            
        Returns:
            Parsed JSON dictionary
            
        Raises:
            ValueError: If response is not valid JSON
            httpx.HTTPError: If API call fails after retries
        """
        last_error = None
        
        for attempt in range(MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ],
                            "temperature": temperature,
                            "response_format": {"type": "json_object"}
                        }
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    
                    # Parse and validate JSON
                    return json.loads(content)
                    
            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code == 429:
                    # Rate limited - wait and retry
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    print(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{MAX_RETRIES}")
                    await asyncio.sleep(wait_time)
                else:
                    raise  # Re-raise non-rate-limit errors
            except json.JSONDecodeError as e:
                raise ValueError(f"LLM returned invalid JSON: {e}")
        
        # All retries exhausted
        raise last_error or Exception("All retries exhausted")
    
    async def generate_text(
        self,
        user_prompt: str,
        system_prompt: str,
        temperature: float = 0.3
    ) -> str:
        """
        Generate plain text response from LLM with retry logic for rate limits.
        
        Args:
            user_prompt: The user message content
            system_prompt: The system instruction
            temperature: Sampling temperature
            
        Returns:
            Text response string
        """
        last_error = None
        
        for attempt in range(MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ],
                            "temperature": temperature
                        }
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                    
            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code == 429:
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    print(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{MAX_RETRIES}")
                    await asyncio.sleep(wait_time)
                else:
                    raise
        
        raise last_error or Exception("All retries exhausted")


# Singleton instance
llm_service = LLMService()
