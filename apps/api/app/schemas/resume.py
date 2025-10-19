from pydantic import BaseModel, HttpUrl
from typing import Optional

class ResumeCreate(BaseModel):
    student_email: str
    raw_text: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None

class ResumeOut(BaseModel):
    id: int
    student_id: int
    source: str

    class Config:
        from_attributes = True
