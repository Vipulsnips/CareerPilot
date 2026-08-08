from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text
from app.services.resume_parser import parse_resume
from app.schemas.resume import ResumeSchema
from app.services.llm_service import parse_resume_with_llm

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeSchema)
async def upload_resume(file: UploadFile = File(...)):
    text = await extract_text(file)
    return parse_resume_with_llm(text);
