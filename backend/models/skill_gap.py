"""Skill Gap Analysis Models - Phase 3 Enhancement."""
from pydantic import BaseModel, Field


class SkillMatch(BaseModel):
    """Individual skill matching result."""
    skill: str
    found_in_cv: bool = False
    source: str = ""  # Where it was found: "skills", "experience", "certifications"


class SkillGapAnalysis(BaseModel):
    """
    Skill gap analysis between CV and JD.
    
    Returned after initial analysis, before user confirmation.
    """
    matched_skills: list[SkillMatch] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    preferred_skills_matched: list[str] = Field(default_factory=list)
    preferred_skills_missing: list[str] = Field(default_factory=list)
    match_percentage: float = 0.0  # 0-100


class ConfirmedSkills(BaseModel):
    """
    User-confirmed skills for tailoring.
    
    Sent by frontend after user toggles missing skills they actually have.
    """
    confirmed_missing_skills: list[str] = Field(default_factory=list)
    # These are skills the JD asked for, user says "yes I have this"


class AnalysisResult(BaseModel):
    """
    Result of initial CV + JD analysis.
    
    Returned before tailoring, contains skill gap for user confirmation.
    """
    cv_parsed: bool = True
    jd_analyzed: bool = True
    company_researched: bool = True
    skill_gap: SkillGapAnalysis
    company_name: str = ""
    role_title: str = ""
