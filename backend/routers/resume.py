from fastapi import APIRouter,UploadFile,File
from services.pdf_service import extract_text

router = APIRouter(
    prefix='/resume',
    tags=["resume"]
)

@router.post("/upload")
async def upload_resume(file:UploadFile = File(...)):
  text=await extract_text(file);
  return {
    "text":text
  }