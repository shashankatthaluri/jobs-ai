"""Agent 2: Company Intelligence Collector - Enhanced.

Extracts company data from Tavily search results with:
- Source link verification
- Reputation/sentiment analysis  
- "Should I Apply?" recommendation
"""
from models.job import CompanyIntelligence, SourceLink, HiringContact
from services.llm import llm_service
from services.tavily import tavily_service


def _clean_intel_response(intel_result: dict) -> dict:
    """
    Clean and validate LLM response before Pydantic parsing.
    
    Handles common LLM mistakes:
    - hiring_contacts as URLs instead of HiringContact objects
    - sources as strings instead of SourceLink objects
    """
    # Clean hiring_contacts - LLM sometimes returns URLs instead of objects
    if "hiring_contacts" in intel_result:
        cleaned_contacts = []
        for contact in intel_result.get("hiring_contacts", []):
            if isinstance(contact, dict):
                # Valid dict - keep it
                cleaned_contacts.append(contact)
            elif isinstance(contact, str):
                # LLM returned a URL or string - convert to proper object
                if contact.startswith("http"):
                    # It's a URL - create a minimal HiringContact
                    cleaned_contacts.append({
                        "name": "",
                        "title": "",
                        "email": "",
                        "source": contact
                    })
                else:
                    # It's some other string - skip it
                    pass
            # Skip any other types
        intel_result["hiring_contacts"] = cleaned_contacts
    
    # Clean sources - ensure they're dicts
    if "sources" in intel_result:
        cleaned_sources = []
        for source in intel_result.get("sources", []):
            if isinstance(source, dict):
                cleaned_sources.append(source)
            elif isinstance(source, str):
                # URL string - convert to SourceLink
                cleaned_sources.append({
                    "title": "",
                    "url": source,
                    "fact": "",
                    "date_found": ""
                })
        intel_result["sources"] = cleaned_sources
    
    return intel_result

# Enhanced prompt with fact-checking and source requirements
COMPANY_INTELLIGENCE_PROMPT = """You are a company research analyst. Your job is to extract VERIFIED facts.

CRITICAL RULES:
1. ONLY use information explicitly stated in the search results
2. DO NOT invent or assume dates, numbers, or facts
3. If a date is unclear, say "undated" - DO NOT guess
4. Include source URLs for key facts
5. Be conservative - only include what you can verify

Return the following JSON:

{
  "company_name": "",
  "website": "",
  "industry": "",
  "employee_count_range": "",
  "company_stage": "",
  "mission": "",
  "recent_funding_or_news": [],
  "sources": [
    {
      "title": "Source page title",
      "url": "https://source-url.com",
      "fact": "What fact this source supports",
      "date_found": "Date if mentioned in source, else empty"
    }
  ],
  "reputation_summary": "",
  "culture_highlights": [],
  "red_flags": [],
  "recommendation": "",
  "confidence_level": "",
  "hiring_contacts": []
}

FIELD GUIDELINES:

* company_stage: "Seed", "Series A/B/C", "Late Stage", "Public", "Established" - from EXPLICIT mentions only
* employee_count_range: Use ranges like "1-50", "51-200", "201-500", "500+". Only if EXPLICITLY stated.
* mission: Company's stated mission, vision, or values. Keep to 1-2 sentences.

* sources: Include URL and specific fact for verification. MINIMUM 2 sources.

* reputation_summary: What employees/users think. Based on reviews, Glassdoor, social mentions.
* culture_highlights: Positive cultural traits (e.g., "Remote-friendly", "Fast-paced", "Strong mentorship")
* red_flags: Any warning signs (layoffs, controversies, bad reviews). Empty if none found.

* recommendation: Brief assessment for job seeker. Examples:
  - "Strong match for growth-oriented candidates. Company is scaling rapidly."
  - "Proceed with caution - recent layoffs reported."
  - "Good reputation in the industry. Stable choice."

* confidence_level: "High" (3+ reliable sources), "Medium" (1-2 sources), "Low" (limited info)

NEVER HALLUCINATE. If information is not in the search results, leave the field empty."""


async def get_company_intelligence(company_name: str) -> CompanyIntelligence:
    """
    Research company using Tavily and extract intelligence.
    """
    if not company_name.strip():
        raise ValueError("Empty company name provided")
    
    try:
        search_results = await tavily_service.search_company(company_name)
        
        search_text = f"Company: {company_name}\n\n"
        search_text += f"Summary: {search_results.get('answer', 'No summary available')}\n\n"
        search_text += "Search Results:\n"
        
        for i, result in enumerate(search_results.get("results", []), 1):
            search_text += f"\n--- Result {i} ---\n"
            search_text += f"Title: {result.get('title', '')}\n"
            search_text += f"URL: {result.get('url', '')}\n"
            search_text += f"Content: {result.get('content', '')}\n"
        
        result = await llm_service.generate_json(
            user_prompt=f"Extract company intelligence from these search results:\n\n{search_text}",
            system_prompt=COMPANY_INTELLIGENCE_PROMPT,
            temperature=0.1
        )
        
        result["company_name"] = company_name
        
        # Ensure sources are properly structured
        if "sources" in result and isinstance(result["sources"], list):
            result["sources"] = [
                SourceLink(**s) if isinstance(s, dict) else s 
                for s in result["sources"]
            ]
        
        return CompanyIntelligence(**result)
        
    except Exception as e:
        raise ValueError(f"Failed to get company intelligence: {e}")


async def get_company_intelligence_from_text(
    company_name: str,
    search_text: str
) -> CompanyIntelligence:
    """
    Extract company intelligence from pre-fetched search text.
    """
    try:
        result = await llm_service.generate_json(
            user_prompt=f"Company: {company_name}\n\nSearch Results:\n{search_text}",
            system_prompt=COMPANY_INTELLIGENCE_PROMPT,
            temperature=0.1
        )
        
        result["company_name"] = company_name
        
        return CompanyIntelligence(**result)
        
    except Exception as e:
        raise ValueError(f"Failed to extract company intelligence: {e}")


async def get_company_intelligence_from_url(company_url: str) -> CompanyIntelligence:
    """
    Research company using deep search from company URL.
    
    Enhanced with:
    - Source URL preservation
    - Reputation/sentiment extraction
    - Recommendation for user
    """
    if not company_url.strip():
        raise ValueError("Empty company URL provided")
    
    try:
        # Deep research from URL
        deep_results = await tavily_service.deep_research_company(company_url)
        company_name = deep_results["company_name"]
        
        # Format with source URLs preserved
        search_text = f"Company: {company_name}\n"
        search_text += f"Website: {company_url}\n\n"
        search_text += f"Summary: {deep_results.get('combined_summary', 'No summary available')}\n\n"
        search_text += "Research Results (note the URLs for sources):\n"
        
        for i, result in enumerate(deep_results.get("results", []), 1):
            search_text += f"\n--- Result {i} ({result.get('query_context', 'general')}) ---\n"
            search_text += f"Title: {result.get('title', '')}\n"
            search_text += f"URL: {result.get('url', '')}\n"
            search_text += f"Content: {result.get('content', '')}\n"
        
        # Extract intelligence using LLM
        result = await llm_service.generate_json(
            user_prompt=f"Extract company intelligence from these deep research results. Include source URLs for verification:\n\n{search_text}",
            system_prompt=COMPANY_INTELLIGENCE_PROMPT,
            temperature=0.1
        )
        
        # Ensure company info is set
        result["company_name"] = company_name
        result["website"] = company_url
        
        # Ensure sources are properly structured
        if "sources" in result and isinstance(result["sources"], list):
            result["sources"] = [
                SourceLink(**s) if isinstance(s, dict) else s 
                for s in result["sources"]
            ]
        
        return CompanyIntelligence(**result)
        
    except Exception as e:
        raise ValueError(f"Failed to get company intelligence from URL: {e}")


async def get_company_intel_with_voice(company_url: str) -> tuple["CompanyIntelligence", "CompanyVoiceProfile"]:
    """
    Research company and extract BOTH intelligence AND voice profile.
    
    This is the primary function for company research, providing:
    - CompanyIntelligence: facts, reputation, recommendation
    - CompanyVoiceProfile: writing style for resume mirroring
    
    Both are extracted from the same deep research to avoid duplicate API calls.
    """
    from agents.voice_extractor import extract_voice_from_research
    from models.job import CompanyVoiceProfile
    
    if not company_url.strip():
        raise ValueError("Empty company URL provided")
    
    try:
        # Deep research from URL (single API call)
        deep_results = await tavily_service.deep_research_company(company_url)
        company_name = deep_results["company_name"]
        
        # Format for intel extraction
        search_text = f"Company: {company_name}\n"
        search_text += f"Website: {company_url}\n\n"
        search_text += f"Summary: {deep_results.get('combined_summary', 'No summary available')}\n\n"
        search_text += "Research Results (note the URLs for sources):\n"
        
        for i, result in enumerate(deep_results.get("results", []), 1):
            search_text += f"\n--- Result {i} ({result.get('query_context', 'general')}) ---\n"
            search_text += f"Title: {result.get('title', '')}\n"
            search_text += f"URL: {result.get('url', '')}\n"
            search_text += f"Content: {result.get('content', '')}\n"
        
        # Extract BOTH intel and voice in parallel-ish manner
        # (Both use same base data, so we call them sequentially but share the research)
        
        # 1. Extract company intelligence
        intel_result = await llm_service.generate_json(
            user_prompt=f"Extract company intelligence from these deep research results. Include source URLs for verification:\n\n{search_text}",
            system_prompt=COMPANY_INTELLIGENCE_PROMPT,
            temperature=0.1
        )
        
        intel_result["company_name"] = company_name
        intel_result["website"] = company_url
        
        # Clean LLM response before Pydantic parsing
        intel_result = _clean_intel_response(intel_result)
        
        # Convert sources to SourceLink objects
        if "sources" in intel_result and isinstance(intel_result["sources"], list):
            intel_result["sources"] = [
                SourceLink(**s) if isinstance(s, dict) else s 
                for s in intel_result["sources"]
            ]
        
        company_intel = CompanyIntelligence(**intel_result)
        
        # 2. Extract voice profile from same research data
        voice_profile = await extract_voice_from_research(deep_results)
        
        return company_intel, voice_profile
        
    except Exception as e:
        raise ValueError(f"Failed to get company intel with voice: {e}")

