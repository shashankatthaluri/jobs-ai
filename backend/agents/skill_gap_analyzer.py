"""Skill Gap Analyzer Agent.

Compares CV skills against JD requirements.
Returns structured gap analysis for user confirmation.
"""
from models.cv import MasterCV
from models.job import JobAnalysis
from models.skill_gap import SkillGapAnalysis, SkillMatch
from services.llm import llm_service


SKILL_GAP_PROMPT = """You are an ATS skill matching specialist.

Inputs:
1. CV skills list
2. CV experience bullets (may contain implicit skills)
3. JD required skills
4. JD preferred skills

Your task:
Analyze which JD skills are present in the CV (explicitly or implicitly).

Rules:
- A skill is "found" if it appears in skills list OR is clearly demonstrated in experience
- Be thorough - skills may be phrased differently (e.g., "Python" vs "Python programming")
- Do NOT assume skills that aren't evidenced
- Output ONLY valid JSON

Return JSON:
{
  "matched_required": [
    {"skill": "Python", "found_in_cv": true, "source": "skills"}
  ],
  "missing_required": ["Kubernetes", "Docker"],
  "matched_preferred": ["GraphQL"],
  "missing_preferred": ["Terraform"],
  "match_percentage": 75
}"""


async def analyze_skill_gap(cv: MasterCV, job: JobAnalysis) -> SkillGapAnalysis:
    """
    Analyze skill gap between CV and JD.
    
    Returns structured analysis for user confirmation UI.
    
    Args:
        cv: Master CV with skills and experience
        job: Job analysis with required and preferred skills
        
    Returns:
        SkillGapAnalysis with matched and missing skills
    """
    # Prepare CV context
    cv_skills = cv.skills
    cv_bullets = []
    for exp in cv.experience:
        cv_bullets.extend(exp.bullets)
    
    user_prompt = f"""Analyze the skill match between this CV and job requirements.

CV SKILLS:
{', '.join(cv_skills)}

CV EXPERIENCE BULLETS:
{chr(10).join(cv_bullets[:20])}

JD REQUIRED SKILLS:
{', '.join(job.required_skills)}

JD PREFERRED SKILLS:
{', '.join(job.preferred_skills)}

Return the skill gap analysis as JSON."""

    try:
        result = await llm_service.generate_json(
            user_prompt=user_prompt,
            system_prompt=SKILL_GAP_PROMPT,
            temperature=0.1
        )
        
        # Build matched skills list
        matched_skills = []
        for item in result.get("matched_required", []):
            if isinstance(item, dict):
                matched_skills.append(SkillMatch(
                    skill=item.get("skill", ""),
                    found_in_cv=True,
                    source=item.get("source", "skills")
                ))
            elif isinstance(item, str):
                matched_skills.append(SkillMatch(skill=item, found_in_cv=True))
        
        # Missing skills
        missing_skills = result.get("missing_required", [])
        if isinstance(missing_skills, list) and len(missing_skills) > 0:
            if isinstance(missing_skills[0], dict):
                missing_skills = [s.get("skill", "") for s in missing_skills]
        
        # Preferred skills
        preferred_matched = result.get("matched_preferred", [])
        if isinstance(preferred_matched, list) and len(preferred_matched) > 0:
            if isinstance(preferred_matched[0], dict):
                preferred_matched = [s.get("skill", "") for s in preferred_matched]
        
        preferred_missing = result.get("missing_preferred", [])
        if isinstance(preferred_missing, list) and len(preferred_missing) > 0:
            if isinstance(preferred_missing[0], dict):
                preferred_missing = [s.get("skill", "") for s in preferred_missing]
        
        return SkillGapAnalysis(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            preferred_skills_matched=preferred_matched,
            preferred_skills_missing=preferred_missing,
            match_percentage=result.get("match_percentage", 0)
        )
        
    except Exception as e:
        raise ValueError(f"Failed to analyze skill gap: {e}")
