"""Job + Company Intelligence API Routes - Phase 2.

Endpoints:
- POST /api/job/analyze - Analyze job description text
- POST /api/job/from-url - Extract + analyze JD from URL
- POST /api/job/company - Get company intelligence
- POST /api/job/process - Full pipeline (JD + Company + Normalize)
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.job import JobAnalysis, CompanyIntelligence, JobCompanyPackage
from agents.jd_analyzer import analyze_job_description
from agents.company_intel import get_company_intelligence
from agents.url_resolver import extract_jd_from_url
from agents.job_normalizer import normalize_job_company_package, get_phase2_warnings


router = APIRouter(prefix="/api/job", tags=["Job Intelligence"])


# Request/Response Models

class AnalyzeJDRequest(BaseModel):
    """Request for JD analysis."""
    jd_text: str


class FromURLRequest(BaseModel):
    """Request for JD extraction from URL."""
    url: str


class CompanyRequest(BaseModel):
    """Request for company intelligence."""
    company_name: str


class ProcessJobRequest(BaseModel):
    """Request for full job + company processing."""
    jd_text: str | None = None
    jd_url: str | None = None
    company_name: str


class ProcessJobResponse(BaseModel):
    """Response from full job processing pipeline."""
    jd_text: str
    job: JobAnalysis
    company: CompanyIntelligence
    package: JobCompanyPackage
    warnings: list[str]


# Endpoints

@router.post("/analyze", response_model=JobAnalysis)
async def analyze_jd(request: AnalyzeJDRequest):
    """
    Agent 1: Analyze job description text.
    
    - Extracts role, skills, requirements
    - Identifies ATS keywords
    - No inference, only explicit data
    """
    try:
        job = await analyze_job_description(request.jd_text)
        return job
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/from-url", response_model=JobAnalysis)
async def analyze_jd_from_url(request: FromURLRequest):
    """
    Agent 3 + 1: Extract JD from URL, then analyze.
    
    - Fetches job posting page
    - Extracts clean JD text
    - Analyzes for requirements
    """
    try:
        # Extract JD from URL
        jd_text = await extract_jd_from_url(request.url)
        
        # Analyze extracted JD
        job = await analyze_job_description(jd_text)
        return job
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/company", response_model=CompanyIntelligence)
async def get_company_info(request: CompanyRequest):
    """
    Agent 2: Get company intelligence.
    
    - Searches using Tavily
    - Extracts factual data only
    - Returns sourced information
    """
    try:
        company = await get_company_intelligence(request.company_name)
        return company
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/process", response_model=ProcessJobResponse)
async def process_job(request: ProcessJobRequest):
    """
    Full Pipeline: JD (text or URL) + Company Intelligence + Normalize.
    
    Chains all Phase 2 agents:
    1. Extract JD from URL (if provided)
    2. Analyze JD
    3. Get company intelligence
    4. Normalize and package
    """
    if not request.jd_text and not request.jd_url:
        raise HTTPException(
            status_code=400,
            detail="Either jd_text or jd_url must be provided"
        )
    
    try:
        # Get JD text
        if request.jd_url:
            jd_text = await extract_jd_from_url(request.jd_url)
        else:
            jd_text = request.jd_text
        
        # Analyze JD
        job = await analyze_job_description(jd_text)
        
        # Get company intelligence
        company = await get_company_intelligence(request.company_name)
        
        # Normalize and package
        package = normalize_job_company_package(job, company)
        warnings = get_phase2_warnings(package)
        
        return ProcessJobResponse(
            jd_text=jd_text,
            job=job,
            company=company,
            package=package,
            warnings=warnings
        )
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "phase": 2}
