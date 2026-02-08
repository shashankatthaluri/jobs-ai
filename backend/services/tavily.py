"""Tavily Search Service for Company Intelligence.

Enhanced for deep company research from URL.
"""
import httpx
import re
from typing import Any
from urllib.parse import urlparse

from config import settings


class TavilySearchService:
    """Async Tavily search client for company research."""
    
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com"
    
    async def search(
        self,
        query: str,
        search_depth: str = "advanced",
        max_results: int = 5,
        include_domains: list[str] | None = None
    ) -> dict[str, Any]:
        """
        Search for information using Tavily.
        
        Args:
            query: Search query
            search_depth: "basic" or "advanced" (more thorough)
            max_results: Maximum number of results
            include_domains: Optional list of domains to prioritize
            
        Returns:
            Search results with title, url, content, and score
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": search_depth,
                "max_results": max_results,
                "include_answer": True
            }
            
            if include_domains:
                payload["include_domains"] = include_domains
            
            response = await client.post(
                f"{self.base_url}/search",
                json=payload
            )
            response.raise_for_status()
            
            return response.json()
    
    def extract_company_name_from_url(self, url: str) -> str:
        """
        Extract company name from URL.
        
        Examples:
            https://stripe.com -> Stripe
            https://www.openai.com -> OpenAI
            https://careers.google.com -> Google
        """
        parsed = urlparse(url if url.startswith('http') else f"https://{url}")
        domain = parsed.netloc.lower()
        
        # Remove www. prefix
        domain = re.sub(r'^www\.', '', domain)
        
        # Remove common subdomains
        domain = re.sub(r'^(careers|jobs|work|hiring|about)\.', '', domain)
        
        # Extract main domain (before TLD)
        parts = domain.split('.')
        if len(parts) >= 2:
            company = parts[0]
        else:
            company = domain
        
        # Capitalize properly
        return company.title()
    
    async def search_company(self, company_name: str) -> dict[str, Any]:
        """
        Search for company information.
        
        Returns structured data about a company including:
        - Website
        - Employee count
        - Recent news/funding
        - Hiring contacts
        """
        query = f"{company_name} company website employees funding news"
        
        results = await self.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
        
        return {
            "query": query,
            "answer": results.get("answer", ""),
            "results": [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                    "score": r.get("score", 0)
                }
                for r in results.get("results", [])
            ]
        }
    
    async def deep_research_company(self, company_url: str) -> dict[str, Any]:
        """
        Deep research a company from its URL.
        
        Performs multiple queries to gather:
        - Company overview and mission
        - Products/services
        - Culture and values
        - Recent news and achievements
        
        Args:
            company_url: Company website URL
            
        Returns:
            Comprehensive company research data
        """
        company_name = self.extract_company_name_from_url(company_url)
        domain = urlparse(company_url if company_url.startswith('http') else f"https://{company_url}").netloc
        
        # Multiple targeted queries for deep research
        queries = [
            f"{company_name} company about mission vision values",
            f"{company_name} products services what they build",
            f"{company_name} company culture work environment employee reviews",
            f"{company_name} recent news funding achievements 2024 2025",
        ]
        
        all_results = []
        combined_answer = []
        
        for query in queries:
            try:
                result = await self.search(
                    query=query,
                    search_depth="advanced",
                    max_results=3,
                    include_domains=[domain] if domain else None
                )
                
                if result.get("answer"):
                    combined_answer.append(result["answer"])
                
                for r in result.get("results", []):
                    all_results.append({
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("content", ""),
                        "score": r.get("score", 0),
                        "query_context": query.split()[2] if len(query.split()) > 2 else "general"
                    })
            except Exception:
                # Continue with other queries if one fails
                continue
        
        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for r in all_results:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                unique_results.append(r)
        
        return {
            "company_name": company_name,
            "company_url": company_url,
            "combined_summary": " ".join(combined_answer),
            "results": unique_results[:10],  # Top 10 unique results
            "research_depth": "deep"
        }


# Singleton instance
tavily_service = TavilySearchService()

