"""Agent 3: CV Validation & Normalization.

Validates structure and normalizes dates.
Does NOT rewrite content - only fixes consistency.
"""
import re
from models.cv import MasterCV, Experience, Education


def normalize_date(date_str: str) -> str:
    """
    Normalize date string to MM/YYYY format.
    
    Handles various input formats:
    - "January 2020" -> "01/2020"
    - "Jan 2020" -> "01/2020"
    - "2020-01" -> "01/2020"
    - "01/2020" -> "01/2020" (unchanged)
    - "Present" -> "Present" (unchanged)
    - "" -> "" (unchanged)
    """
    if not date_str or date_str.strip() == "":
        return ""
    
    date_str = date_str.strip()
    
    # Already in correct format or special value
    if re.match(r"^\d{2}/\d{4}$", date_str) or date_str.lower() in ["present", "current", "now"]:
        return date_str
    
    # Month name mappings
    months = {
        "january": "01", "jan": "01",
        "february": "02", "feb": "02",
        "march": "03", "mar": "03",
        "april": "04", "apr": "04",
        "may": "05",
        "june": "06", "jun": "06",
        "july": "07", "jul": "07",
        "august": "08", "aug": "08",
        "september": "09", "sep": "09", "sept": "09",
        "october": "10", "oct": "10",
        "november": "11", "nov": "11",
        "december": "12", "dec": "12"
    }
    
    # Try "Month YYYY" format
    for month_name, month_num in months.items():
        pattern = rf"^{month_name}\s+(\d{{4}})$"
        match = re.match(pattern, date_str.lower())
        if match:
            return f"{month_num}/{match.group(1)}"
    
    # Try "YYYY-MM" format
    match = re.match(r"^(\d{4})-(\d{2})$", date_str)
    if match:
        return f"{match.group(2)}/{match.group(1)}"
    
    # Try "MM-YYYY" format
    match = re.match(r"^(\d{2})-(\d{4})$", date_str)
    if match:
        return f"{match.group(1)}/{match.group(2)}"
    
    # Try "YYYY" only (assume January)
    match = re.match(r"^(\d{4})$", date_str)
    if match:
        return f"01/{match.group(1)}"
    
    # Return original if no pattern matches
    return date_str


def validate_experience(exp: Experience) -> Experience:
    """Validate and normalize a single experience entry."""
    return Experience(
        company=exp.company.strip() if exp.company else "",
        role=exp.role.strip() if exp.role else "",
        start_date=normalize_date(exp.start_date),
        end_date=normalize_date(exp.end_date),
        bullets=[b.strip() for b in exp.bullets if b.strip()]
    )


def validate_education(edu: Education) -> Education:
    """Validate and normalize a single education entry."""
    return Education(
        institution=edu.institution.strip() if edu.institution else "",
        degree=edu.degree.strip() if edu.degree else "",
        start_date=normalize_date(edu.start_date),
        end_date=normalize_date(edu.end_date)
    )


def validate_cv(cv: MasterCV) -> MasterCV:
    """
    Validate and normalize MasterCV structure.
    
    This agent does NOT rewrite content.
    It only:
    - Normalizes date formats
    - Strips whitespace
    - Ensures arrays are arrays
    - Validates required structure
    
    Args:
        cv: MasterCV object to validate
        
    Returns:
        Validated and normalized MasterCV
    """
    # Normalize experience entries
    validated_experience = [
        validate_experience(exp)
        for exp in cv.experience
    ]
    
    # Normalize education entries
    validated_education = [
        validate_education(edu)
        for edu in cv.education
    ]
    
    # Normalize skills (strip whitespace, remove empty)
    validated_skills = [
        skill.strip()
        for skill in cv.skills
        if skill.strip()
    ]
    
    return MasterCV(
        name=cv.name.strip() if cv.name else "",
        email=cv.email.strip() if cv.email else "",
        phone=cv.phone.strip() if cv.phone else "",
        location=cv.location.strip() if cv.location else "",
        summary=cv.summary.strip() if cv.summary else "",
        experience=validated_experience,
        skills=validated_skills,
        education=validated_education
    )


def get_validation_warnings(cv: MasterCV) -> list[str]:
    """
    Get warnings for missing critical fields.
    
    Returns list of warning messages (does not modify CV).
    """
    warnings = []
    
    if not cv.name:
        warnings.append("Missing: name")
    
    if not cv.email:
        warnings.append("Missing: email")
    
    if not cv.experience:
        warnings.append("Missing: experience (no work history found)")
    
    for i, exp in enumerate(cv.experience):
        if not exp.company:
            warnings.append(f"Experience #{i+1}: missing company name")
        if not exp.role:
            warnings.append(f"Experience #{i+1}: missing role/title")
    
    if not cv.skills:
        warnings.append("Missing: skills")
    
    return warnings
