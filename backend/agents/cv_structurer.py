"""Agent 2: CV Structuring.

Converts raw resume text into canonical structured JSON.
No guessing, no filling gaps, no hallucination.
"""
from models.cv import MasterCV
from services.llm import llm_service


# LOCKED PROMPT - DO NOT MODIFY
CV_STRUCTURING_PROMPT = """You are a senior resume parsing engineer.

Input: Raw text extracted from a resume.

Your task:
1. Extract resume data into structured JSON.
2. Preserve exact wording from the resume.
3. Preserve exact dates, company names, and roles.
4. Do NOT infer missing information.
5. Do NOT add or remove experience.
6. If a field is missing, use an empty string "" or empty array [].

Rules:
- Experience must be in reverse chronological order.
- Bullets must remain verbatim (rewrite NOTHING).
- Output ONLY valid JSON.
- No commentary, no markdown.

Use this exact JSON schema:
{
  "name": "",
  "email": "",
  "phone": "",
  "location": "",
  "summary": "",
  "experience": [
    {
      "company": "",
      "role": "",
      "start_date": "",
      "end_date": "",
      "bullets": []
    }
  ],
  "skills": [],
  "education": [
    {
      "institution": "",
      "degree": "",
      "start_date": "",
      "end_date": ""
    }
  ]
}"""


async def structure_cv(raw_text: str) -> MasterCV:
    """
    Convert raw resume text to structured MasterCV JSON.
    
    Args:
        raw_text: Plain text extracted from resume PDF
        
    Returns:
        MasterCV object with structured data
        
    Raises:
        ValueError: If structuring fails
    """
    if not raw_text.strip():
        raise ValueError("Empty resume text provided")
    
    try:
        # Call LLM to structure the CV
        result = await llm_service.generate_json(
            user_prompt=f"Parse this resume:\n\n{raw_text}",
            system_prompt=CV_STRUCTURING_PROMPT,
            temperature=0.1  # Low temperature for consistency
        )
        
        # Validate against schema
        cv = MasterCV(**result)
        
        return cv
        
    except Exception as e:
        raise ValueError(f"Failed to structure CV: {e}")
