"""Matching and Tailoring Models - Phase 3."""
from pydantic import BaseModel, Field


class RelevantExperience(BaseModel):
    """Experience entry scored for relevance to job."""
    company: str = ""
    role: str = ""
    relevance_score: int = 0  # 0-100
    matched_skills: list[str] = Field(default_factory=list)
    relevant_bullets: list[str] = Field(default_factory=list)


class MatchingResult(BaseModel):
    """
    CV ↔ JD matching analysis.
    
    Internal planning JSON - decides what to keep/drop/rewrite.
    """
    relevant_experience: list[RelevantExperience] = Field(default_factory=list)
    matched_skills: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    irrelevant_experience: list[str] = Field(default_factory=list)


class RewrittenExperience(BaseModel):
    """Experience with ATS-optimized bullets."""
    company: str = ""
    role: str = ""
    start_date: str = ""
    end_date: str = ""
    bullets: list[str] = Field(default_factory=list)


class RewriteResult(BaseModel):
    """Result of bullet rewriting."""
    rewritten_experience: list[RewrittenExperience] = Field(default_factory=list)


class TailoredResume(BaseModel):
    """
    Final tailored resume package.
    
    Contains markdown resume and metadata.
    """
    resume_markdown: str = ""
    matched_skills: list[str] = Field(default_factory=list)
    keywords_used: list[str] = Field(default_factory=list)
    relevance_summary: str = ""
