"""Writing Layer Models - Phase 4."""
from pydantic import BaseModel


class CoverLetter(BaseModel):
    """Generated cover letter."""
    content: str = ""
    word_count: int = 0


class ColdEmail(BaseModel):
    """Generated cold email."""
    content: str = ""
    word_count: int = 0


class CompanySummary(BaseModel):
    """Human-readable company intelligence summary."""
    content: str = ""
    word_count: int = 0


class WritingPackage(BaseModel):
    """Complete writing outputs for user."""
    cover_letter: CoverLetter
    cold_email: ColdEmail
    company_summary: CompanySummary
