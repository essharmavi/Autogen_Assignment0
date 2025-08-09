from pydantic import BaseModel, Field
from typing import List, Optional


class JobDescription(BaseModel):
    job_profile: str = Field(..., description="Job title or role being offered")
    experience: str = Field(..., description="Required experience for the job")
    skills: List[str] = Field(..., description="List of required skills")
    company_name: str = Field(..., description="Name of the company offering the job")
    location: str = Field(..., description="Job location")
    additional_requirements: str = Field(..., description="Any additional requirements")

    model_config = {
        "extra": "forbid",  
    }


class Questionnaire(BaseModel):
    title: str
    questions: List[str]  
