"""Agents package."""
# Phase 1 - CV Processing
from .pdf_extractor import extract_text_from_pdf
from .cv_structurer import structure_cv
from .cv_validator import validate_cv

# Phase 2 - Job + Company Intelligence
from .jd_analyzer import analyze_job_description
from .company_intel import get_company_intelligence, get_company_intelligence_from_text
from .url_resolver import extract_jd_from_url
from .job_normalizer import normalize_job_company_package, get_phase2_warnings

# Phase 3 - CV Matching & Tailoring
from .cv_matcher import analyze_cv_job_match
from .bullet_rewriter import rewrite_bullets
from .resume_generator import generate_ats_resume

# Phase 4 - Writing Layer
from .cover_letter import generate_cover_letter
from .cold_email import generate_cold_email
from .company_summary import generate_company_summary

__all__ = [
    # Phase 1
    "extract_text_from_pdf",
    "structure_cv",
    "validate_cv",
    # Phase 2
    "analyze_job_description",
    "get_company_intelligence",
    "get_company_intelligence_from_text",
    "extract_jd_from_url",
    "normalize_job_company_package",
    "get_phase2_warnings",
    # Phase 3
    "analyze_cv_job_match",
    "rewrite_bullets",
    "generate_ats_resume",
    # Phase 4
    "generate_cover_letter",
    "generate_cold_email",
    "generate_company_summary"
]
