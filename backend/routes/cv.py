"""CV Processing API Routes.

Phase 1 endpoints:
- POST /api/cv/extract - PDF → Raw Text
- POST /api/cv/structure - Raw Text → JSON
- POST /api/cv/validate - Validate JSON
- POST /api/cv/process - Full pipeline (chains all 3)
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel

from models.cv import MasterCV
from agents.pdf_extractor import extract_text_from_pdf
from agents.cv_structurer import structure_cv
from agents.cv_validator import validate_cv, get_validation_warnings


router = APIRouter(prefix="/api/cv", tags=["CV Processing"])


# Request/Response Models
class ExtractResponse(BaseModel):
    """Response from text extraction."""
    raw_text: str
    char_count: int


class StructureRequest(BaseModel):
    """Request for CV structuring."""
    raw_text: str


class ValidateRequest(BaseModel):
    """Request for CV validation."""
    cv: MasterCV


class ProcessResponse(BaseModel):
    """Response from full CV processing pipeline."""
    raw_text: str
    cv: MasterCV
    warnings: list[str]


# Endpoints

@router.post("/extract", response_model=ExtractResponse)
async def extract_cv_text(file: UploadFile = File(...)):
    """
    Agent 1: Extract raw text from PDF resume.
    
    - Accepts PDF file upload
    - Returns plain text preserving original order
    - No summarization or interpretation
    """
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )
    
    # Read file bytes
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read file: {e}"
        )
    
    # Extract text
    try:
        raw_text = extract_text_from_pdf(contents)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    
    return ExtractResponse(
        raw_text=raw_text,
        char_count=len(raw_text)
    )


@router.post("/structure", response_model=MasterCV)
async def structure_cv_text(request: StructureRequest):
    """
    Agent 2: Structure raw text into Master CV JSON.
    
    - Accepts raw resume text
    - Returns structured JSON matching locked schema
    - No hallucination, no inference
    """
    try:
        cv = await structure_cv(request.raw_text)
        return cv
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )


@router.post("/validate", response_model=MasterCV)
async def validate_cv_json(request: ValidateRequest):
    """
    Agent 3: Validate and normalize CV JSON.
    
    - Normalizes date formats
    - Validates structure
    - Does NOT rewrite content
    """
    validated = validate_cv(request.cv)
    return validated


@router.post("/process", response_model=ProcessResponse)
async def process_cv(file: UploadFile = File(...)):
    """
    Full Pipeline: Extract → Structure → Validate.
    
    Chains all 3 agents to process a PDF resume end-to-end.
    Returns the validated Master CV JSON ready for downstream use.
    """
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )
    
    # Read file
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read file: {e}"
        )
    
    # Agent 1: Extract
    try:
        raw_text = extract_text_from_pdf(contents)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"PDF extraction failed: {e}"
        )
    
    # Agent 2: Structure
    try:
        cv = await structure_cv(raw_text)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"CV structuring failed: {e}"
        )
    
    # Agent 3: Validate
    validated_cv = validate_cv(cv)
    warnings = get_validation_warnings(validated_cv)
    
    return ProcessResponse(
        raw_text=raw_text,
        cv=validated_cv,
        warnings=warnings
    )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "phase": 1}
