"""Master CV data models - LOCKED SCHEMA."""
from pydantic import BaseModel, Field


class Experience(BaseModel):
    """Work experience entry."""
    company: str = ""
    role: str = ""
    start_date: str = ""
    end_date: str = ""
    bullets: list[str] = Field(default_factory=list)


class Education(BaseModel):
    """Education entry."""
    institution: str = ""
    degree: str = ""
    start_date: str = ""
    end_date: str = ""


class MasterCV(BaseModel):
    """
    Master CV schema - LOCKED.
    
    This is the canonical representation of a parsed resume.
    All fields preserve exact wording from the original document.
    No inference, no hallucination.
    """
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    summary: str = ""
    experience: list[Experience] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1-555-123-4567",
                "location": "San Francisco, CA",
                "summary": "Experienced software engineer...",
                "experience": [
                    {
                        "company": "Tech Corp",
                        "role": "Senior Engineer",
                        "start_date": "01/2020",
                        "end_date": "Present",
                        "bullets": [
                            "Led team of 5 engineers",
                            "Reduced latency by 40%"
                        ]
                    }
                ],
                "skills": ["Python", "FastAPI", "React"],
                "education": [
                    {
                        "institution": "MIT",
                        "degree": "B.S. Computer Science",
                        "start_date": "09/2012",
                        "end_date": "05/2016"
                    }
                ]
            }
        }
