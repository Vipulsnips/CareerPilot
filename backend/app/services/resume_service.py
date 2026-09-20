from fastapi import UploadFile

from app.services.pdf_service import extract_text
from app.services.llm_service import parse_resume_with_llm
from app.services.analysis_service import analyse_resume
from app.logging_config import logger
from app.services.rag.ingestion_service import index_resume

async def process_resume(
    file: UploadFile,
    user_id: str,
):
    logger.info(
        "Resume processing started",
        extra={"event": "resume_processing_started"},
    )

    text = await extract_text(file)
    index_resume(text=text,user_id=user_id)
    resume = parse_resume_with_llm(text)
    analysis = analyse_resume(resume)

    logger.info(
        "Resume processing completed",
        extra={"event": "resume_processing_completed"},
    )

    return {"resume": resume, "analysis": analysis}
