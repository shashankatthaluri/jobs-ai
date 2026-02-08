"""Agent 1: CV ↔ JD Matching & Relevance Analyzer.

Compares Master CV against Job requirements.
Decides what experience is relevant, what skills match.
Zero hallucination - only uses what exists in CV.
"""
import json
from models.cv import MasterCV
from models.job import JobAnalysis
from models.tailoring import MatchingResult
from services.llm import llm_service


# LOCKED PROMPT - DO NOT MODIFY
MATCHING_PROMPT = """You are an ATS optimization engine.

Inputs:
1. Master CV JSON (READ-ONLY)
2. Job analysis JSON

Your task:
1. Compare job requirements against CV experience.
2. Identify which experience entries are MOST relevant.
3. Identify matching skills.
4. Identify missing job keywords NOT present in the CV.
5. Do NOT invent skills or experience.

Return the following JSON:

{
  "relevant_experience": [
    {
      "company": "",
      "role": "",
      "relevance_score": 0,
      "matched_skills": [],
      "relevant_bullets": []
    }
  ],
  "matched_skills": [],
  "missing_keywords": [],
  "irrelevant_experience": []
}

Rules:
- relevance_score is 0–100 based on job fit.
- relevant_bullets must be copied verbatim from CV.
- Missing keywords must be factual and common role terms.
- Do NOT rewrite any text.
- Output ONLY valid JSON.
- No explanations."""


async def analyze_cv_job_match(cv: MasterCV, job: JobAnalysis) -> MatchingResult:
    """
    Analyze CV against job requirements.
    
    This is the "brain" step - decides what to keep, drop, emphasize.
    
    Args:
        cv: Master CV JSON (read-only)
        job: Job analysis JSON
        
    Returns:
        MatchingResult with relevance scores and matched skills
    """
    # Prepare CV and job as JSON strings
    cv_json = cv.model_dump_json(indent=2)
    job_json = job.model_dump_json(indent=2)
    
    user_prompt = f"""Analyze the match between this CV and job requirements.

MASTER CV:
{cv_json}

JOB REQUIREMENTS:
{job_json}

Return the matching analysis as JSON."""
    
    try:
        result = await llm_service.generate_json(
            user_prompt=user_prompt,
            system_prompt=MATCHING_PROMPT,
            temperature=0.1
        )
        
        return MatchingResult(**result)
        
    except Exception as e:
        raise ValueError(f"Failed to analyze CV-job match: {e}")
