"""Agent: Cold Email Generator.

Generates short, human cold emails for job seekers reaching out to companies.
Friendly but professional, expresses genuine interest, clear CTA.
"""
from models.job import JobAnalysis, CompanyIntelligence, HiringContact
from models.writing import ColdEmail
from services.llm import llm_service


# FIXED PROMPT - Job seeker perspective (not recruiter)
COLD_EMAIL_PROMPT = """You are helping a JOB SEEKER write a cold email to a company they want to work for.

CRITICAL: The email is FROM the candidate TO the company. The candidate is reaching out to express interest in a role.

Inputs:
1. Candidate summary (their background)
2. Job role they're interested in
3. Company information
4. Hiring contact (if available)

Your task:
Write a short, confident cold email from the job seeker's perspective.

Structure:
1. Brief introduction of who you are
2. Why you're excited about THIS company (be specific)
3. One or two relevant experiences that make you a fit
4. Clear ask (call, chat, or consideration for the role)

Rules:
- Use first person ("I" statements)
- 4 to 6 sentences only
- Confident but not arrogant
- Show you researched the company
- One clear CTA (ask for a quick call or chat)
- No desperation ("I really need this job")
- No buzzwords ("synergy", "passionate", "rockstar")
- No generic flattery

Tone:
- Professional but human
- Like a warm LinkedIn message from a peer
- Enthusiastic about the opportunity, not begging

Constraints:
- Max 100 words
- If no contact name, use "Hi there" or "Hello"

Output:
- Plain text email only
- No subject line
- No explanations
- No signature block"""


async def generate_cold_email(
    candidate_summary: str,
    job: JobAnalysis,
    company: CompanyIntelligence,
    hiring_contact: HiringContact | None = None
) -> ColdEmail:
    """
    Generate cold outreach email from job seeker to company.
    
    Args:
        candidate_summary: Short summary from resume
        job: Job analysis JSON
        company: Company intelligence JSON
        hiring_contact: Optional hiring contact info
        
    Returns:
        ColdEmail with content and word count
    """
    contact_info = ""
    greeting_suggestion = ""
    if hiring_contact and hiring_contact.name:
        contact_info = f"Hiring Contact: {hiring_contact.name}, {hiring_contact.title}"
        greeting_suggestion = f"Address the email to {hiring_contact.name}"
    else:
        contact_info = "No specific contact known"
        greeting_suggestion = "Use a warm general greeting"
    
    # Extract company hook
    company_hook = ""
    if company.mission:
        company_hook = f"Company Mission: {company.mission}"
    elif company.culture_highlights:
        company_hook = f"Company Culture: {', '.join(company.culture_highlights[:3])}"
    
    user_prompt = f"""Write a cold email FROM a job seeker TO this company.

ABOUT THE CANDIDATE (who is writing this email):
{candidate_summary}

TARGET JOB:
Role: {job.role_title}
Company: {company.company_name}
Industry: {company.industry}

{company_hook}

{contact_info}
{greeting_suggestion}

Remember: The candidate is reaching out to express interest in joining the company. Write in first person from their perspective."""

    try:
        content = await llm_service.generate_text(
            user_prompt=user_prompt,
            system_prompt=COLD_EMAIL_PROMPT,
            temperature=0.5
        )
        
        content = content.strip()
        word_count = len(content.split())
        
        return ColdEmail(content=content, word_count=word_count)
        
    except Exception as e:
        raise ValueError(f"Failed to generate cold email: {e}")
