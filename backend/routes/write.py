"""Writing Layer API Routes - Phase 4.

Endpoints:
- POST /api/write/cover-letter - Generate cover letter
- POST /api/write/cold-email - Generate cold email
- POST /api/write/company-summary - Generate company summary
- POST /api/write/all - Generate all writing outputs
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.job import JobAnalysis, CompanyIntelligence, HiringContact
from models.writing import CoverLetter, ColdEmail, CompanySummary, WritingPackage
from agents.cover_letter import generate_cover_letter
from agents.cold_email import generate_cold_email
from agents.company_summary import generate_company_summary


router = APIRouter(prefix="/api/write", tags=["Writing Layer"])


# Request Models

class CoverLetterRequest(BaseModel):
    """Request for cover letter generation."""
    resume_markdown: str
    job: JobAnalysis
    company: CompanyIntelligence


class ColdEmailRequest(BaseModel):
    """Request for cold email generation."""
    candidate_summary: str
    job: JobAnalysis
    company: CompanyIntelligence
    hiring_contact: HiringContact | None = None


class CompanySummaryRequest(BaseModel):
    """Request for company summary generation."""
    company: CompanyIntelligence


class FullWritingRequest(BaseModel):
    """Request for all writing outputs."""
    resume_markdown: str
    candidate_summary: str
    job: JobAnalysis
    company: CompanyIntelligence
    hiring_contact: HiringContact | None = None


# Endpoints

@router.post("/cover-letter", response_model=CoverLetter)
async def create_cover_letter(request: CoverLetterRequest):
    """
    Generate personalized cover letter.
    
    - Max 350 words
    - 3 paragraphs
    - Professional tone
    """
    try:
        result = await generate_cover_letter(
            request.resume_markdown,
            request.job,
            request.company
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/cold-email", response_model=ColdEmail)
async def create_cold_email(request: ColdEmailRequest):
    """
    Generate cold outreach email.
    
    - Max 120 words
    - 4-6 sentences
    - Clear CTA
    """
    try:
        result = await generate_cold_email(
            request.candidate_summary,
            request.job,
            request.company,
            request.hiring_contact
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/company-summary", response_model=CompanySummary)
async def create_company_summary(request: CompanySummaryRequest):
    """
    Generate human-readable company summary.
    
    - Max 150 words
    - Factual, neutral tone
    """
    try:
        result = await generate_company_summary(request.company)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/all", response_model=WritingPackage)
async def create_all_writing(request: FullWritingRequest):
    """
    Generate all writing outputs.
    
    Returns cover letter, cold email, and company summary.
    """
    try:
        cover_letter = await generate_cover_letter(
            request.resume_markdown,
            request.job,
            request.company
        )
        
        cold_email = await generate_cold_email(
            request.candidate_summary,
            request.job,
            request.company,
            request.hiring_contact
        )
        
        company_summary = await generate_company_summary(request.company)
        
        return WritingPackage(
            cover_letter=cover_letter,
            cold_email=cold_email,
            company_summary=company_summary
        )
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "phase": 4}
