"""Job and Company Intelligence Models - Phase 2 Enhanced.

Extended with source links, reputation, and recommendation for user decision-making.
"""
from pydantic import BaseModel, Field


class HiringContact(BaseModel):
    """Publicly available hiring contact."""
    name: str = ""
    title: str = ""
    email: str = ""
    source: str = ""


class SourceLink(BaseModel):
    """Verified source with URL for fact-checking."""
    title: str = ""
    url: str = ""
    fact: str = ""  # What fact this source supports
    date_found: str = ""  # When in the source text (if mentioned)


class JobAnalysis(BaseModel):
    """
    Structured job description analysis.
    
    Enhanced with must-have vs nice-to-have skills.
    """
    role_title: str = ""
    department: str = ""
    seniority_level: str = ""
    employment_type: str = ""
    
    # Skill categorization
    must_have_skills: list[str] = Field(default_factory=list)
    nice_to_have_skills: list[str] = Field(default_factory=list)
    unclear_skills: list[str] = Field(default_factory=list)  # For user to clarify
    
    # Legacy fields (keep for compatibility)
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    
    responsibilities: list[str] = Field(default_factory=list)
    keywords_for_ats: list[str] = Field(default_factory=list)
    industry: str = ""
    
    # Years of experience requirement
    years_experience_required: str = ""  # e.g., "3-5 years", "5+ years"


class CompanyIntelligence(BaseModel):
    """
    Company research data with source verification.
    
    Extended to include:
    - Source links for fact verification
    - Reputation/sentiment analysis
    - "Should I Apply?" recommendation
    """
    company_name: str = ""
    website: str = ""
    industry: str = ""
    employee_count_range: str = ""
    company_stage: str = ""
    mission: str = ""
    
    # News with source links
    recent_funding_or_news: list[str] = Field(default_factory=list)
    
    # Source verification (NEW)
    sources: list[SourceLink] = Field(default_factory=list)
    
    # Reputation/Sentiment (NEW)
    reputation_summary: str = ""  # What people think (from reviews, social)
    culture_highlights: list[str] = Field(default_factory=list)  # e.g., "Remote-friendly", "Fast-paced"
    red_flags: list[str] = Field(default_factory=list)  # Warning signs
    
    # Decision helper (NEW)
    recommendation: str = ""  # Should user apply? Brief assessment
    confidence_level: str = ""  # "High", "Medium", "Low" - based on source quality
    
    # Hiring info
    hiring_contacts: list[HiringContact] = Field(default_factory=list)


class CompanyVoiceProfile(BaseModel):
    """
    Company writing style for resume mirroring.
    
    Captures HOW the company writes, not just WHAT they say.
    Used to transform resume bullets to match company tone.
    """
    # Sentence structure
    sentence_style: str = ""  # "short_punchy" | "detailed" | "balanced"
    avg_sentence_length: str = ""  # "short" (<15 words) | "medium" | "long"
    
    # Voice characteristics
    ownership_level: str = ""  # "strong" (I owned, Led) | "moderate" | "passive"
    metric_emphasis: str = ""  # "heavy" | "moderate" | "light"
    
    # Tone
    tone: str = ""  # "aggressive" | "collaborative" | "formal" | "casual"
    
    # Value vocabulary (actual words to mirror)
    value_vocabulary: list[str] = Field(default_factory=list)
    # e.g., ["customer-obsessed", "ownership", "bias for action"]
    
    # Sample phrases (examples of their writing style)
    sample_phrases: list[str] = Field(default_factory=list)
    # e.g., ["Own end-to-end", "Customer-first approach"]
    
    # Writing instructions for LLM
    style_instructions: str = ""
    # Specific guidance for bullet rewriting


class JobCompanyPackage(BaseModel):
    """
    Combined job + company intelligence.
    
    Ready for Phase 3 matching engine.
    """
    job: JobAnalysis
    company: CompanyIntelligence
