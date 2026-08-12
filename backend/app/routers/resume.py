from fastapi import APIRouter, UploadFile, File

from app.services.resume_service import process_resume


router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    return await process_resume(file)