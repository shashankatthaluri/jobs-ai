"""Agent 4: Job + Company Normalizer.

Final validation layer before Phase 3.
Validates structure, normalizes formatting.
Does NOT rewrite content.
"""
from models.job import JobAnalysis, CompanyIntelligence, JobCompanyPackage


def normalize_string(s: str) -> str:
    """Normalize string: strip whitespace, normalize spacing."""
    if not s:
        return ""
    return " ".join(s.split()).strip()


def normalize_list(items: list[str]) -> list[str]:
    """Normalize list: strip items, remove empty."""
    return [normalize_string(item) for item in items if item and item.strip()]


def normalize_job_analysis(job: JobAnalysis) -> JobAnalysis:
    """
    Normalize job analysis data.
    
    - Strips whitespace
    - Removes empty items from lists
    - Normalizes casing for specific fields
    """
    return JobAnalysis(
        role_title=normalize_string(job.role_title),
        department=normalize_string(job.department),
        seniority_level=normalize_string(job.seniority_level),
        employment_type=normalize_string(job.employment_type),
        required_skills=normalize_list(job.required_skills),
        preferred_skills=normalize_list(job.preferred_skills),
        responsibilities=normalize_list(job.responsibilities),
        keywords_for_ats=normalize_list(job.keywords_for_ats),
        industry=normalize_string(job.industry)
    )


def normalize_company_intelligence(company: CompanyIntelligence) -> CompanyIntelligence:
    """
    Normalize company intelligence data.
    
    - Strips whitespace
    - Normalizes URLs
    - Cleans hiring contacts
    """
    # Normalize hiring contacts
    normalized_contacts = []
    for contact in company.hiring_contacts:
        if contact.name or contact.email:  # Keep if has name or email
            normalized_contacts.append({
                "name": normalize_string(contact.name),
                "title": normalize_string(contact.title),
                "email": normalize_string(contact.email).lower() if contact.email else "",
                "source": normalize_string(contact.source)
            })
    
    return CompanyIntelligence(
        company_name=normalize_string(company.company_name),
        website=normalize_string(company.website).lower() if company.website else "",
        industry=normalize_string(company.industry),
        employee_count_range=normalize_string(company.employee_count_range),
        company_stage=normalize_string(company.company_stage),
        recent_funding_or_news=normalize_list(company.recent_funding_or_news),
        hiring_contacts=normalized_contacts
    )


def normalize_job_company_package(
    job: JobAnalysis,
    company: CompanyIntelligence
) -> JobCompanyPackage:
    """
    Normalize and combine job + company data.
    
    Final validation before Phase 3.
    
    Args:
        job: JobAnalysis object
        company: CompanyIntelligence object
        
    Returns:
        Normalized JobCompanyPackage
    """
    return JobCompanyPackage(
        job=normalize_job_analysis(job),
        company=normalize_company_intelligence(company)
    )


def get_phase2_warnings(package: JobCompanyPackage) -> list[str]:
    """
    Get warnings for missing critical fields.
    
    Returns list of warning messages.
    """
    warnings = []
    
    # Job warnings
    if not package.job.role_title:
        warnings.append("Job: Missing role title")
    
    if not package.job.required_skills:
        warnings.append("Job: No required skills found")
    
    if not package.job.keywords_for_ats:
        warnings.append("Job: No ATS keywords extracted")
    
    # Company warnings
    if not package.company.company_name:
        warnings.append("Company: Missing company name")
    
    if not package.company.website:
        warnings.append("Company: Website not found")
    
    return warnings
