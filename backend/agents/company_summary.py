"""Agent 3: Company Intelligence Summary.

Converts raw company JSON into human-readable summary.
Factual, neutral, no speculation.
"""
from models.job import CompanyIntelligence
from models.writing import CompanySummary
from services.llm import llm_service


# LOCKED PROMPT - DO NOT MODIFY
COMPANY_SUMMARY_PROMPT = """You are a business analyst summarizing company intelligence for a job seeker.

Input:
Company intelligence JSON.

Your task:
Summarize the company in a factual, neutral tone.

Rules:
- Do NOT speculate.
- Do NOT hype the company.
- Mention:
  - What the company does
  - Approximate size
  - Recent news or funding (if available)
  - Hiring context (if known)

Constraints:
- Max 150 words.
- Clear, simple language.

Output:
- Plain text summary only.
- No explanations."""


async def generate_company_summary(company: CompanyIntelligence) -> CompanySummary:
    """
    Generate human-readable company summary.
    
    Args:
        company: Company intelligence JSON
        
    Returns:
        CompanySummary with content and word count
    """
    user_prompt = f"""Summarize this company for a job seeker.

COMPANY INTELLIGENCE:
Name: {company.company_name}
Website: {company.website}
Industry: {company.industry}
Size: {company.employee_count_range}
Stage: {company.company_stage}
Recent News: {', '.join(company.recent_funding_or_news) if company.recent_funding_or_news else 'None available'}
Hiring Contacts: {len(company.hiring_contacts)} found

Write the summary now."""

    try:
        content = await llm_service.generate_text(
            user_prompt=user_prompt,
            system_prompt=COMPANY_SUMMARY_PROMPT,
            temperature=0.3
        )
        
        content = content.strip()
        word_count = len(content.split())
        
        return CompanySummary(content=content, word_count=word_count)
        
    except Exception as e:
        raise ValueError(f"Failed to generate company summary: {e}")
