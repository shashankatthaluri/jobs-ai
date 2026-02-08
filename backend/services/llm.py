"""LLM Service for JSON generation."""
import json
import httpx
from typing import Any

from config import settings


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
        Generate JSON response from LLM.
        
        Args:
            user_prompt: The user message content
            system_prompt: The system instruction
            temperature: Sampling temperature (lower = more deterministic)
            
        Returns:
            Parsed JSON dictionary
            
        Raises:
            ValueError: If response is not valid JSON
            httpx.HTTPError: If API call fails
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
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
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                raise ValueError(f"LLM returned invalid JSON: {e}")
    
    async def generate_text(
        self,
        user_prompt: str,
        system_prompt: str,
        temperature: float = 0.3
    ) -> str:
        """
        Generate plain text response from LLM.
        
        Args:
            user_prompt: The user message content
            system_prompt: The system instruction
            temperature: Sampling temperature
            
        Returns:
            Text response string
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
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


# Singleton instance
llm_service = LLMService()
