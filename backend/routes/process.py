"""End-to-End Processing Route - Phase 5.

Orchestrates all 4 phases into a single workflow.
"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import Optional

from models.cv import MasterCV
from models.job import JobAnalysis, CompanyIntelligence, JobCompanyPackage
from models.tailoring import MatchingResult, RewriteResult, TailoredResume
from models.writing import WritingPackage

from agents.pdf_extractor import extract_text_from_pdf
from agents.cv_structurer import structure_cv
from agents.cv_validator import validate_cv, get_validation_warnings

from agents.url_resolver import extract_jd_from_url
from agents.jd_analyzer import analyze_job_description
from agents.company_intel import get_company_intelligence

from agents.cv_matcher import analyze_cv_job_match
from agents.bullet_rewriter import rewrite_bullets
from agents.resume_generator import generate_ats_resume

from agents.cover_letter import generate_cover_letter
from agents.cold_email import generate_cold_email
from agents.company_summary import generate_company_summary


router = APIRouter(prefix="/api/process", tags=["End-to-End Processing"])


class FullProcessResponse(BaseModel):
    """Combined response for the entire application process."""
    master_cv: MasterCV
    job_analysis: JobAnalysis
    company_intel: CompanyIntelligence
    tailored_resume: TailoredResume
    writing: WritingPackage
    warnings: list[str]


@router.post("/all", response_model=FullProcessResponse)
async def process_all(
    cv_pdf: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    job_url: Optional[str] = Form(None),
    company_name: str = Form(...)
):
    """
    End-to-End Orchestration:
    1. Parse PDF → Master CV
    2. Extract Job Info (Text or URL)
    3. Research Company
    4. Match & Tailor Resume
    5. Generate Cover Letter, Email, and Summary
    """
    if not job_description and not job_url:
        raise HTTPException(
            status_code=400,
            detail="Either job_description or job_url must be provided"
        )

    try:
        # --- PHASE 1: Master CV Intelligence ---
        # Agent 1: Extract Text
        cv_contents = await cv_pdf.read()
        raw_cv_text = extract_text_from_pdf(cv_contents)
        
        # Agent 2: Structure
        cv_json = await structure_cv(raw_cv_text)
        
        # Agent 3: Validate
        master_cv = validate_cv(cv_json)
        cv_warnings = get_validation_warnings(master_cv)

        # --- PHASE 2: Job + Company Intelligence ---
        # Agent 3: URL Resolver (if needed)
        clean_jd_text = ""
        if job_url:
            clean_jd_text = await extract_jd_from_url(job_url)
        else:
            clean_jd_text = job_description

        # Agent 1: JD Analysis
        job_analysis = await analyze_job_description(clean_jd_text)

        # Agent 2: Company Intelligence
        company_intel = await get_company_intelligence(company_name)

        # --- PHASE 3: Matching + Tailoring ---
        # Agent 1: Match
        matching_result = await analyze_cv_job_match(master_cv, job_analysis)
        
        # Agent 2: Bullet Rewriting
        rewritten_result = await rewrite_bullets(
            master_cv, 
            matching_result, 
            job_analysis.keywords_for_ats
        )
        
        # Agent 3: Resume Generation
        tailored_resume = await generate_ats_resume(
            master_cv,
            rewritten_result,
            matching_result.matched_skills,
            job_analysis.keywords_for_ats
        )

        # --- PHASE 4: Writing Layer ---
        # Agent 1: Cover Letter
        cover_letter = await generate_cover_letter(
            tailored_resume.resume_markdown,
            job_analysis,
            company_intel
        )
        
        # Agent 2: Cold Email
        cold_email = await generate_cold_email(
            master_cv.summary, # Using master summary for general fit
            job_analysis,
            company_intel
        )
        
        # Agent 3: Company Summary
        company_summary = await generate_company_summary(company_intel)
        
        writing_package = WritingPackage(
            cover_letter=cover_letter,
            cold_email=cold_email,
            company_summary=company_summary
        )

        return FullProcessResponse(
            master_cv=master_cv,
            job_analysis=job_analysis,
            company_intel=company_intel,
            tailored_resume=tailored_resume,
            writing=writing_package,
            warnings=cv_warnings
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Log error in real world, for now just pass it
        raise HTTPException(status_code=500, detail=str(e))
