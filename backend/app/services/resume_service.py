from fastapi import UploadFile

from app.services.pdf_service import extract_text
from app.services.llm_service import parse_resume_with_llm
from app.services.analysis_service import analyse_resume


async def process_resume(file: UploadFile):
    text = await extract_text(file)

    resume = parse_resume_with_llm(text)
    analysis = analyse_resume(resume)

    return {
        "resume": resume,
        "analysis": analysis,
    }