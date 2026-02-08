"""Agent 3: ATS Resume Generator - Enhanced with Company Intelligence.

Generates clean, ATS-compatible resume in markdown.
Uses company philosophy and culture to predict ATS optimization priorities.
"""
from models.cv import MasterCV
from models.tailoring import RewriteResult, TailoredResume
from models.job import CompanyIntelligence
from services.llm import llm_service


def _derive_ats_priorities_from_company(company_intel: CompanyIntelligence | None) -> str:
    """
    Use company philosophy/culture to predict their ATS prioritization.
    
    Key insight: Companies design their ATS filters to match their values.
    - Innovation-focused companies: prioritize creativity, new tech keywords
    - Process-driven companies: prioritize methodologies, certifications
    - Growth-stage startups: prioritize impact/metrics, adaptability
    - Enterprise: prioritize stability, scale, compliance
    """
    if not company_intel:
        return "Standard ATS optimization - focus on role-specific keywords."
    
    priorities = []
    
    # Analyze company stage
    stage = (company_intel.company_stage or "").lower()
    if "startup" in stage or "seed" in stage or "series a" in stage:
        priorities.append("Emphasize adaptability, wearing multiple hats, rapid iteration, impact metrics")
    elif "growth" in stage or "series b" in stage or "series c" in stage:
        priorities.append("Balance innovation with process; emphasize scaling, team leadership, measurable results")
    else:
        priorities.append("Emphasize stability, large-scale experience, cross-functional collaboration")
    
    # Analyze industry for domain keywords
    industry = (company_intel.industry or "").lower()
    if "tech" in industry or "software" in industry:
        priorities.append("Technical depth and modern stack keywords are critical")
    elif "finance" in industry or "banking" in industry:
        priorities.append("Compliance, accuracy, regulatory awareness keywords matter")
    elif "health" in industry or "medical" in industry:
        priorities.append("Precision, patient care, regulatory compliance keywords important")
    elif "retail" in industry or "commerce" in industry:
        priorities.append("Customer experience, conversion, growth metrics valued")
    
    # Company size impacts expectations
    size = (company_intel.employee_count_range or "").lower()
    if "1-50" in size or "1-10" in size or "10-50" in size:
        priorities.append("Generalist skills valued; show autonomy and ownership")
    elif "500+" in size or "1000+" in size or "5000+" in size:
        priorities.append("Specialist depth valued; show collaboration across teams")
    
    # Use mission/values if available for cultural keywords
    if company_intel.mission:
        priorities.append(f"Align language with company values: {company_intel.mission[:200]}")
    
    return "\n".join(priorities) if priorities else "Standard ATS optimization."


# ENHANCED PROMPT - Company-aware ATS optimization
ATS_RESUME_PROMPT = """You are an expert ATS resume generator with company intelligence integration.

Your goal: Create a resume that maximizes ATS pass rate for THIS SPECIFIC company.

CRITICAL ATS RULES:
1. ONE-COLUMN LAYOUT - No tables, no columns, no graphics
2. STANDARD SECTION HEADINGS: Summary, Experience, Skills, Education
3. REVERSE CHRONOLOGICAL ORDER within each section
4. SIMPLE BULLET POINTS using hyphens (-) only
5. EXACT KEYWORD MATCHING - Use the exact job keywords provided
6. QUANTIFIED ACHIEVEMENTS - Numbers, percentages, dollar amounts
7. NO CREATIVE FORMATTING - ATS cannot parse fancy elements
8. CONTACT INFO AT TOP - Name, email, phone, location on separate lines

RESUME TEMPLATE STRUCTURE:
```
# [FULL NAME]
[email] | [phone] | [location]

## Summary
[2-3 sentences highlighting relevant experience and key value proposition]

## Experience

### [Job Title] | [Company Name]
[Start Date] - [End Date]
- [Achievement with metric] using [relevant keywords]
- [Achievement with metric] demonstrating [skill from job requirements]
- [Achievement with metric] resulting in [business impact]

### [Previous Job Title] | [Previous Company]
[Start Date] - [End Date]
- [Relevant achievement]
- [Relevant achievement]

## Skills
[Skill 1], [Skill 2], [Skill 3], ... (matched skills FIRST, then others)

## Education
[Degree] - [Institution] ([Year])
```

COMPANY-SPECIFIC OPTIMIZATION:
{company_priorities}

LENGTH GUIDANCE (CRITICAL):
- DEFAULT to 1 page. This is the target for most candidates.
- Recruiters scan for 6-8 seconds. One clean, dense page wins over two sparse pages.
- Expand to 2 pages ONLY if you would be cutting real measurable achievements to stay at 1 page.

How to decide:
1. Count the candidate's RELEVANT roles with quantified achievements
2. If 1-2 roles with strong bullets → 1 page
3. If 3+ roles with genuine metrics and outcomes → 2 pages is acceptable
4. NEVER exceed 2 pages. Beyond that is noise.

Quality over quantity:
- 4 strong bullets per role > 8 weak bullets
- Cut generic responsibilities, keep measurable impact
- If a bullet doesn't show outcome or skill match, cut it

The real rule: Use 1 page until you're CUTTING REAL ACHIEVEMENTS to stay there.

IMPORTANT:
- Do NOT invent experience, metrics, or dates
- Do NOT add skills the candidate doesn't have
- PRESERVE all original dates and titles exactly
- Focus on ACTUAL achievements, properly worded for ATS"""


async def generate_ats_resume(
    cv: MasterCV,
    rewritten: RewriteResult,
    matched_skills: list[str],
    job_keywords: list[str],
    company_intel: CompanyIntelligence | None = None
) -> TailoredResume:
    """
    Generate company-aware ATS-optimized resume.
    
    Args:
        cv: Original Master CV
        rewritten: Rewritten experience with optimized bullets
        matched_skills: Skills that match the job
        job_keywords: Keywords for ATS optimization
        company_intel: Company research for culture-aware optimization
        
    Returns:
        TailoredResume with markdown and metadata
    """
    # Derive ATS priorities from company philosophy
    company_priorities = _derive_ats_priorities_from_company(company_intel)
    
    # Prepare system prompt with company context
    system_prompt = ATS_RESUME_PROMPT.format(company_priorities=company_priorities)
    
    # Prepare structured inputs
    cv_contact = {
        "name": cv.name,
        "email": cv.email,
        "phone": cv.phone,
        "location": cv.location,
        "summary": cv.summary
    }
    
    education_list = [
        {
            "institution": edu.institution,
            "degree": edu.degree,
            "start_date": edu.start_date,
            "end_date": edu.end_date
        }
        for edu in cv.education
    ]
    
    # All skills with matched ones first (ATS prioritization)
    all_skills = list(matched_skills)
    for skill in cv.skills:
        if skill not in all_skills:
            all_skills.append(skill)
    
    # Include company context in user prompt
    company_context = ""
    if company_intel:
        company_context = f"""
COMPANY CONTEXT:
- Company: {company_intel.company_name}
- Industry: {company_intel.industry}
- Stage: {company_intel.company_stage}
- Size: {company_intel.employee_count_range}
- Mission: {company_intel.mission or 'N/A'}
"""
    
    user_prompt = f"""Generate an ATS-optimized resume for this candidate targeting this specific company.

CONTACT INFO:
{cv_contact}

REWRITTEN EXPERIENCE (use these optimized bullets):
{rewritten.model_dump_json(indent=2)}

SKILLS TO PRIORITIZE (matched skills, ordered by importance):
{all_skills}

JOB KEYWORDS (MUST appear in resume):
{job_keywords}

EDUCATION:
{education_list}
{company_context}
Generate the resume in clean markdown format following the exact template structure."""
    
    try:
        resume_md = await llm_service.generate_text(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.15  # Lower temp for more consistent ATS format
        )
        
        # Calculate relevance summary
        exp_count = len(rewritten.rewritten_experience)
        skills_count = len(matched_skills)
        keywords_count = len(job_keywords)
        
        company_name = company_intel.company_name if company_intel else "target company"
        
        relevance_summary = (
            f"ATS-optimized resume for {company_name} with {exp_count} tailored experience entries, "
            f"{skills_count} matched skills, and {keywords_count} job-specific keywords."
        )
        
        return TailoredResume(
            resume_markdown=resume_md.strip(),
            matched_skills=matched_skills,
            keywords_used=job_keywords,
            relevance_summary=relevance_summary
        )
        
    except Exception as e:
        raise ValueError(f"Failed to generate resume: {e}")
