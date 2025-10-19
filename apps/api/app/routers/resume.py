from fastapi import APIRouter, UploadFile, Form, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from pydantic import BaseModel, HttpUrl
from typing import Optional

from ..db.session import get_session
from ..models.student import Student
from ..models.resume import Resume, EMBEDDING_DIM
from ..services.embeddings import embed_texts

router = APIRouter()

class ResumeIn(BaseModel):
    student_email: str
    linkedin_url: Optional[HttpUrl] = None
    raw_text: Optional[str] = None

@router.post("/parse")
async def parse_resume(payload: ResumeIn, db: AsyncSession = Depends(get_session)):
    has_text = bool(payload.raw_text and payload.raw_text.strip())
    has_link = bool(payload.linkedin_url)
    if not (has_text or has_link):
        raise HTTPException(status_code=400, detail="Provide raw_text or linkedin_url.")

    # 1) ensure student exists (by email)
    stmt = select(Student).where(Student.email == payload.student_email)
    result = await db.execute(stmt)
    student = result.scalar_one_or_none()
    if not student:
        res = await db.execute(insert(Student).values(email=payload.student_email).returning(Student))
        student = res.scalar_one()

    # 2) derive source + text
    source = "text" if has_text else "linkedin"
    text = payload.raw_text or str(payload.linkedin_url)

    # 3) embed
    vecs = embed_texts([text])
    embedding = vecs[0] if vecs else None

    # 4) insert resume
    res_ins = await db.execute(
        insert(Resume).values(
            student_id=student.id,
            source=source,
            raw_text=text if has_text else None,
            embedding=embedding,
        ).returning(Resume.id)
    )
    resume_id = res_ins.scalar_one()
    await db.commit()
    return {"id": resume_id, "student_id": student.id, "source": source, "embedded": embedding is not None}

@router.post("/upload")
async def upload_resume(file: UploadFile, student_id: str = Form(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing file.")
    # TODO: persist file, OCR/PDF-to-text, then same flow as /parse
    return {"received": file.filename, "student_id": student_id}
