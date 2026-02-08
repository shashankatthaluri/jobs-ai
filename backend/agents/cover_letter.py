"""Agent 1: Cover Letter Generator - Enhanced.

Generates personalized cover letters using:
- Company mission/culture from intelligence
- Recent news/achievements as talking points
- Cultural alignment hooks
"""
from models.job import JobAnalysis, CompanyIntelligence
from models.writing import CoverLetter
from services.llm import llm_service


# Enhanced prompt with company culture integration
COVER_LETTER_PROMPT = """You are a career coach crafting a compelling, personalized cover letter.

PERSONALIZATION IS KEY. Use the company intelligence to:
1. Reference their MISSION or VALUES in your opening
2. Mention a RECENT ACHIEVEMENT or NEWS (if provided)
3. Show CULTURAL ALIGNMENT with their work environment
4. Demonstrate you've researched them specifically

STRUCTURE (3 paragraphs max):

PARAGRAPH 1 - THE HOOK:
- Open with something specific about the company (news, mission, product)
- Transition to why you're excited about this role
- Do NOT start with "I am writing to apply..."

PARAGRAPH 2 - YOUR VALUE:
- 2-3 specific achievements that match their requirements
- Use metrics from the resume when possible
- Connect your experience to their specific needs

PARAGRAPH 3 - THE CLOSE:
- Brief statement of cultural fit
- Clear call to action
- Confident, not desperate tone

RULES:
- Max 300 words (hiring managers skim)
- NO generic phrases: "passionate", "hard-working", "team player"
- NO "I believe I would be a great fit"
- SHOW don't tell - use specific examples
- Reference company by name at least once
- Sound like a human, not a template

OUTPUT: Plain text cover letter only. No explanations."""


async def generate_cover_letter(
    resume_markdown: str,
    job: JobAnalysis,
    company: CompanyIntelligence
) -> CoverLetter:
    """
    Generate personalized cover letter using company intelligence.
    """
    # Build company context for personalization
    company_context = f"Company: {company.company_name}\n"
    company_context += f"Industry: {company.industry}\n"
    company_context += f"Size: {company.employee_count_range}\n"
    
    if company.mission:
        company_context += f"Mission/Values: {company.mission}\n"
    
    if company.culture_highlights:
        company_context += f"Culture: {', '.join(company.culture_highlights)}\n"
    
    if company.recent_funding_or_news:
        news = company.recent_funding_or_news[0] if company.recent_funding_or_news else ""
        company_context += f"Recent News: {news}\n"
    
    # Get skills - prefer must_have if available
    skills = job.must_have_skills if job.must_have_skills else job.required_skills
    key_skills = ', '.join(skills[:5]) if skills else "Not specified"
    
    user_prompt = f"""Write a personalized cover letter for this application.

COMPANY INTELLIGENCE (use this for personalization):
{company_context}

JOB DETAILS:
Role: {job.role_title}
Department: {job.department}
Seniority: {job.seniority_level}
Must-Have Skills: {key_skills}
{f"Experience Required: {job.years_experience_required}" if job.years_experience_required else ""}

CANDIDATE'S TAILORED RESUME:
{resume_markdown}

IMPORTANT: The opening paragraph MUST reference something specific about {company.company_name} - their mission, recent news, or product. Make them feel like this letter was written JUST for them.

Write the cover letter now."""

    try:
        content = await llm_service.generate_text(
            user_prompt=user_prompt,
            system_prompt=COVER_LETTER_PROMPT,
            temperature=0.5  # Slightly higher for more natural variation
        )
        
        content = content.strip()
        word_count = len(content.split())
        
        return CoverLetter(content=content, word_count=word_count)
        
    except Exception as e:
        raise ValueError(f"Failed to generate cover letter: {e}")
