"""LLM Service with Groq primary and OpenRouter fallback."""
import json
import httpx
import logging
from typing import Any

from config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Async LLM client with automatic failover between providers."""
    
    def __init__(self):
        # Primary: Groq
        self.primary_api_key = settings.LLM_API_KEY
        self.primary_base_url = settings.LLM_BASE_URL
        self.primary_model = settings.LLM_MODEL
        
        # Fallback: OpenRouter
        self.fallback_api_key = settings.OPENROUTER_API_KEY
        self.fallback_base_url = settings.OPENROUTER_BASE_URL
        self.fallback_model = settings.OPENROUTER_MODEL
    
    async def _call_provider(
        self,
        base_url: str,
        api_key: str,
        model: str,
        messages: list[dict],
        temperature: float,
        json_mode: bool = False,
        provider_name: str = "unknown"
    ) -> dict:
        """Make API call to a specific provider."""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # OpenRouter requires additional headers
        if "openrouter" in base_url.lower():
            headers["HTTP-Referer"] = "https://jobstudio.petgharcare.com"
            headers["X-Title"] = "Jobs AI"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def _generate_with_fallback(
        self,
        messages: list[dict],
        temperature: float,
        json_mode: bool = False
    ) -> str:
        """Try primary provider, fallback to secondary on failure."""
        
        # Try Groq (primary)
        if self.primary_api_key:
            try:
                logger.info(f"Trying Groq with model: {self.primary_model}")
                data = await self._call_provider(
                    self.primary_base_url,
                    self.primary_api_key,
                    self.primary_model,
                    messages,
                    temperature,
                    json_mode,
                    "Groq"
                )
                logger.info("Groq request successful")
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    logger.warning("Groq rate limited, falling back to OpenRouter")
                else:
                    logger.warning(f"Groq error ({e.response.status_code}), falling back to OpenRouter")
            except Exception as e:
                logger.warning(f"Groq failed: {e}, falling back to OpenRouter")
        
        # Try OpenRouter (fallback)
        if self.fallback_api_key:
            try:
                logger.info(f"Trying OpenRouter with model: {self.fallback_model}")
                data = await self._call_provider(
                    self.fallback_base_url,
                    self.fallback_api_key,
                    self.fallback_model,
                    messages,
                    temperature,
                    json_mode,
                    "OpenRouter"
                )
                logger.info("OpenRouter request successful")
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"OpenRouter also failed: {e}")
                raise
        
        raise ValueError("No LLM provider available. Check API keys.")
    
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
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        content = await self._generate_with_fallback(messages, temperature, json_mode=True)
        
        # Parse and validate JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
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
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return await self._generate_with_fallback(messages, temperature, json_mode=False)


# Singleton instance
llm_service = LLMService()
