"""Multi-Step Analysis Routes - Enhanced with Voice Mirroring.

Splits the processing into:
1. /analyze - CV parsing + JD analysis + skill gap + voice profile
2. /tailor - Final tailoring with confirmed skills AND voice mirroring
"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import Optional

from models.cv import MasterCV
from models.job import JobAnalysis, CompanyIntelligence, CompanyVoiceProfile
from models.skill_gap import SkillGapAnalysis, ConfirmedSkills

from agents.pdf_extractor import extract_text_from_pdf
from agents.cv_structurer import structure_cv
from agents.cv_validator import validate_cv, get_validation_warnings

from agents.url_resolver import extract_jd_from_url
from agents.jd_analyzer import analyze_job_description
from agents.company_intel import get_company_intel_with_voice, get_company_intelligence_from_url
from agents.skill_gap_analyzer import analyze_skill_gap


router = APIRouter(prefix="/api/analyze", tags=["Multi-Step Analysis"])


class AnalysisResponse(BaseModel):
    """Response from initial analysis step."""
    master_cv: MasterCV
    job_analysis: JobAnalysis
    company_intel: CompanyIntelligence
    voice_profile: CompanyVoiceProfile  # NEW
    skill_gap: SkillGapAnalysis
    cv_warnings: list[str]


@router.post("/step1", response_model=AnalysisResponse)
async def analyze_step1(
    cv_pdf: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    job_url: Optional[str] = Form(None),
    company_url: str = Form(...)
):
    """
    Step 1: Initial Analysis
    
    - Parse CV
    - Analyze JD
    - Research company (from URL) + extract voice profile
    - Analyze skill gap
    
    Returns skill gap and voice profile for user confirmation before tailoring.
    """
    if not job_description and not job_url:
        raise HTTPException(
            status_code=400,
            detail="Either job_description or job_url must be provided"
        )

    try:
        # --- PHASE 1: Master CV Intelligence ---
        cv_contents = await cv_pdf.read()
        raw_cv_text = extract_text_from_pdf(cv_contents)
        cv_json = await structure_cv(raw_cv_text)
        master_cv = validate_cv(cv_json)
        cv_warnings = get_validation_warnings(master_cv)

        # --- PHASE 2: Job + Company Intelligence ---
        clean_jd_text = ""
        if job_url:
            clean_jd_text = await extract_jd_from_url(job_url)
        else:
            clean_jd_text = job_description

        # Analyze JD
        job_analysis = await analyze_job_description(clean_jd_text)

        # Deep company research + voice extraction (single call for efficiency)
        company_intel, voice_profile = await get_company_intel_with_voice(company_url)

        # --- PHASE 3: Skill Gap Analysis ---
        skill_gap = await analyze_skill_gap(master_cv, job_analysis)

        return AnalysisResponse(
            master_cv=master_cv,
            job_analysis=job_analysis,
            company_intel=company_intel,
            voice_profile=voice_profile,  # NEW
            skill_gap=skill_gap,
            cv_warnings=cv_warnings
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TailorRequest(BaseModel):
    """Request for tailoring with confirmed skills and voice profile."""
    master_cv: MasterCV
    job_analysis: JobAnalysis
    company_intel: CompanyIntelligence
    voice_profile: Optional[CompanyVoiceProfile] = None  # NEW
    confirmed_skills: ConfirmedSkills


class TailorResponse(BaseModel):
    """Response from tailoring step."""
    resume_markdown: str
    cover_letter: str
    cold_email: str
    company_summary: str
    keywords_used: list[str]
    matched_skills: list[str]


@router.post("/step2/tailor", response_model=TailorResponse)
async def tailor_step2(request: TailorRequest):
    """
    Step 2: Tailoring with Confirmed Skills + Voice Mirroring
    
    Takes the analysis from step 1 plus user-confirmed skills.
    Generates tailored resume with company voice mirroring.
    """
    from agents.cv_matcher import analyze_cv_job_match
    from agents.bullet_rewriter import rewrite_bullets
    from agents.resume_generator import generate_ats_resume
    from agents.cover_letter import generate_cover_letter
    from agents.cold_email import generate_cold_email
    from agents.company_summary import generate_company_summary
    
    try:
        # Add confirmed skills to CV skills list
        enhanced_cv = request.master_cv.model_copy(deep=True)
        for skill in request.confirmed_skills.confirmed_missing_skills:
            if skill not in enhanced_cv.skills:
                enhanced_cv.skills.append(skill)
        
        # --- Matching + Tailoring ---
        matching_result = await analyze_cv_job_match(enhanced_cv, request.job_analysis)
        
        # Rewrite bullets WITH voice mirroring
        rewritten_result = await rewrite_bullets(
            enhanced_cv,
            matching_result,
            request.job_analysis.keywords_for_ats,
            request.voice_profile  # VOICE MIRRORING
        )
        
        tailored_resume = await generate_ats_resume(
            enhanced_cv,
            rewritten_result,
            matching_result.matched_skills,
            request.job_analysis.keywords_for_ats,
            request.company_intel
        )

        # --- Writing Layer ---
        cover_letter = await generate_cover_letter(
            tailored_resume.resume_markdown,
            request.job_analysis,
            request.company_intel
        )
        
        cold_email = await generate_cold_email(
            enhanced_cv.summary,
            request.job_analysis,
            request.company_intel
        )
        
        company_summary = await generate_company_summary(request.company_intel)

        return TailorResponse(
            resume_markdown=tailored_resume.resume_markdown,
            cover_letter=cover_letter.content,
            cold_email=cold_email.content,
            company_summary=company_summary.content,
            keywords_used=tailored_resume.keywords_used,
            matched_skills=tailored_resume.matched_skills
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
