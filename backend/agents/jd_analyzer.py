"""Agent 1: Job Description Analyzer - Enhanced.

Converts raw JD text into structured hiring intelligence with:
- Must-have vs nice-to-have skill separation
- Unclear skills for user clarification
- Years of experience extraction
"""
from models.job import JobAnalysis
from services.llm import llm_service


# Enhanced prompt with better skill categorization
JD_ANALYSIS_PROMPT = """You are a senior technical recruiter and ATS specialist.

Input: A job description text.

Your task:
1. Analyze the job description carefully
2. Categorize skills into MUST-HAVE vs NICE-TO-HAVE
3. Identify any skills that are UNCLEAR (need user input)
4. Extract years of experience requirements

Return the following structured JSON:

{
  "role_title": "",
  "department": "",
  "seniority_level": "",
  "employment_type": "",
  "years_experience_required": "",
  
  "must_have_skills": [],
  "nice_to_have_skills": [],
  "unclear_skills": [],
  
  "required_skills": [],
  "preferred_skills": [],
  
  "responsibilities": [],
  "keywords_for_ats": [],
  "industry": ""
}

SKILL CATEGORIZATION RULES:

1. MUST-HAVE SKILLS - Skills that are:
   - Listed under "Required", "Requirements", "Qualifications"
   - Stated with "must have", "required", "essential"
   - Stated with "X+ years of experience in..."
   - Mentioned multiple times throughout the JD

2. NICE-TO-HAVE SKILLS - Skills that are:
   - Listed under "Preferred", "Nice to have", "Bonus"
   - Stated with "preferred", "ideally", "nice to have", "plus", "bonus"
   - Mentioned only once in passing

3. UNCLEAR SKILLS - Skills that are:
   - Mentioned without clear requirement level
   - Listed in a way that could be either required or preferred
   - Generic skills that might not be key for the role

YEARS OF EXPERIENCE:
- Extract explicit mentions like "5+ years", "3-5 years"
- If stated as "Senior" without years, estimate "5+ years"
- If stated as "Junior" without years, estimate "0-2 years"
- If unclear, leave empty

KEYWORDS FOR ATS:
- Include ALL technical terms, tools, methodologies
- Include industry jargon and role-specific terms
- Include both abbreviated and full forms (e.g., "AWS" and "Amazon Web Services")

OTHER RULES:
- Preserve wording as close to the JD as possible
- Do NOT add skills not mentioned in the JD
- If a field is not present, return empty string or empty array
- Output ONLY valid JSON
- No explanations, no markdown

ALSO populate required_skills and preferred_skills (for backward compatibility):
- required_skills = same as must_have_skills
- preferred_skills = same as nice_to_have_skills"""


async def analyze_job_description(jd_text: str) -> JobAnalysis:
    """
    Analyze job description and extract structured data.
    
    Enhanced with must-have vs nice-to-have skill separation.
    """
    if not jd_text.strip():
        raise ValueError("Empty job description provided")
    
    try:
        result = await llm_service.generate_json(
            user_prompt=f"Analyze this job description and categorize skills carefully:\n\n{jd_text}",
            system_prompt=JD_ANALYSIS_PROMPT,
            temperature=0.1
        )
        
        # Ensure backward compatibility
        if not result.get("required_skills") and result.get("must_have_skills"):
            result["required_skills"] = result["must_have_skills"]
        if not result.get("preferred_skills") and result.get("nice_to_have_skills"):
            result["preferred_skills"] = result["nice_to_have_skills"]
        
        return JobAnalysis(**result)
        
    except Exception as e:
        raise ValueError(f"Failed to analyze job description: {e}")
