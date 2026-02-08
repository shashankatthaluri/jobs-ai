"""CV Tailoring API Routes - Phase 3.

Endpoints:
- POST /api/tailor/match - Analyze CV-JD match
- POST /api/tailor/rewrite - Rewrite bullets for ATS
- POST /api/tailor/generate - Generate ATS resume
- POST /api/tailor/process - Full tailoring pipeline
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.cv import MasterCV
from models.job import JobAnalysis
from models.tailoring import MatchingResult, RewriteResult, TailoredResume
from agents.cv_matcher import analyze_cv_job_match
from agents.bullet_rewriter import rewrite_bullets
from agents.resume_generator import generate_ats_resume


router = APIRouter(prefix="/api/tailor", tags=["Resume Tailoring"])


# Request/Response Models

class MatchRequest(BaseModel):
    """Request for CV-JD matching."""
    cv: MasterCV
    job: JobAnalysis


class RewriteRequest(BaseModel):
    """Request for bullet rewriting."""
    cv: MasterCV
    matching: MatchingResult
    job_keywords: list[str]


class GenerateRequest(BaseModel):
    """Request for resume generation."""
    cv: MasterCV
    rewritten: RewriteResult
    matched_skills: list[str]
    job_keywords: list[str]


class FullTailorRequest(BaseModel):
    """Request for full tailoring pipeline."""
    cv: MasterCV
    job: JobAnalysis


class FullTailorResponse(BaseModel):
    """Response from full tailoring pipeline."""
    matching: MatchingResult
    rewritten: RewriteResult
    resume: TailoredResume


# Endpoints

@router.post("/match", response_model=MatchingResult)
async def match_cv_to_job(request: MatchRequest):
    """
    Step 3.1: Analyze CV-JD match.
    
    - Scores experience relevance
    - Identifies matched skills
    - Finds missing keywords
    - Internal planning layer
    """
    try:
        result = await analyze_cv_job_match(request.cv, request.job)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/rewrite", response_model=RewriteResult)
async def rewrite_cv_bullets(request: RewriteRequest):
    """
    Step 3.2: Rewrite bullets for ATS.
    
    - Optimizes selected bullets
    - Injects keywords where truthful
    - Preserves meaning and facts
    """
    try:
        result = await rewrite_bullets(
            request.cv,
            request.matching,
            request.job_keywords
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/generate", response_model=TailoredResume)
async def generate_resume(request: GenerateRequest):
    """
    Step 3.3: Generate ATS-safe resume.
    
    - One-column markdown layout
    - Standard headings
    - Prioritized skills
    """
    try:
        result = await generate_ats_resume(
            request.cv,
            request.rewritten,
            request.matched_skills,
            request.job_keywords
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/process", response_model=FullTailorResponse)
async def full_tailoring_pipeline(request: FullTailorRequest):
    """
    Full Pipeline: Match → Rewrite → Generate.
    
    Chains all Phase 3 agents:
    1. Analyze CV-JD match
    2. Rewrite relevant bullets
    3. Generate ATS-safe resume
    """
    try:
        # Step 1: Match
        matching = await analyze_cv_job_match(request.cv, request.job)
        
        # Get job keywords
        job_keywords = request.job.keywords_for_ats
        
        # Step 2: Rewrite
        rewritten = await rewrite_bullets(
            request.cv,
            matching,
            job_keywords
        )
        
        # Step 3: Generate
        resume = await generate_ats_resume(
            request.cv,
            rewritten,
            matching.matched_skills,
            job_keywords
        )
        
        return FullTailorResponse(
            matching=matching,
            rewritten=rewritten,
            resume=resume
        )
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "phase": 3}
