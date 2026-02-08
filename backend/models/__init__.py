"""Models package."""
from .cv import MasterCV, Experience, Education
from .job import JobAnalysis, CompanyIntelligence, JobCompanyPackage, HiringContact
from .tailoring import MatchingResult, RewriteResult, TailoredResume, RelevantExperience, RewrittenExperience
from .writing import CoverLetter, ColdEmail, CompanySummary, WritingPackage

__all__ = [
    "MasterCV", "Experience", "Education",
    "JobAnalysis", "CompanyIntelligence", "JobCompanyPackage", "HiringContact",
    "MatchingResult", "RewriteResult", "TailoredResume", "RelevantExperience", "RewrittenExperience",
    "CoverLetter", "ColdEmail", "CompanySummary", "WritingPackage"
]
