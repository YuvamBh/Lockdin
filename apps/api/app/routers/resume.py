from fastapi import APIRouter, UploadFile, Form, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional

router = APIRouter()

class ResumeIn(BaseModel):
    linkedin_url: Optional[HttpUrl] = None
    raw_text: Optional[str] = None

@router.post("/parse")
async def parse_resume(payload: ResumeIn):
    """
    MVP stub:
      - accepts LinkedIn URL OR raw text
      - returns whether we received something usable
    Next version will:
      - extract text
      - embed
      - store in DB
    """
    has_text = bool(payload.raw_text and payload.raw_text.strip())
    has_link = bool(payload.linkedin_url)
    if not (has_text or has_link):
        raise HTTPException(status_code=400, detail="Provide raw_text or linkedin_url.")
    return {"parsed": True, "source": "text" if has_text else "linkedin"}

@router.post("/upload")
async def upload_resume(file: UploadFile, student_id: str = Form(...)):
    """
    MVP stub:
      - accepts a file upload
      - just returns filename + student_id
    Next version will:
      - persist file to storage
      - enqueue parse task
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing file.")
    return {"received": file.filename, "student_id": student_id}
