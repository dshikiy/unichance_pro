from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserRequest(BaseModel):
    ielts: float = Field(default=0.0, ge=0, le=9.0)
    sat: Optional[int] = Field(default=None, ge=400, le=1600)
    gpa: float = Field(default=0.0, ge=0, le=4.0)
    major: Optional[str] = Field(None)
    country: Optional[str] = Field("Any")
    require_full_grant: bool = Field(False)

class ScholarshipBase(BaseModel):
    id: int
    type: str
    description: str

    class Config:
        from_attributes = True

class ProgramBase(BaseModel):
    id: int
    name: str
    degree: str
    min_sat: Optional[int]
    min_ielts: float
    gpa_min: float
    deadline: Optional[str]
    has_full_grant: bool
    scholarships: List[ScholarshipBase] = []

    class Config:
        from_attributes = True

class UniversityBase(BaseModel):
    id: int
    name: str
    country: str
    city: str
    description: str
    website: str
    programs: List[ProgramBase] = []

    class Config:
        from_attributes = True

class CalculationResult(BaseModel):
    program_id: int
    university_name: str
    university_country: str
    university_city: str
    university_website: str
    program_name: str
    degree: str
    chance: float
    level: str
    has_full_grant: bool
    deadline: Optional[str]