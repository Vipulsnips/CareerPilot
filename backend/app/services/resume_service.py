from fastapi import UploadFile

from app.schemas.analysis import ResumeAnalysis
from app.schemas.questions import InterviewQuestions
from app.schemas.resume import ResumeSchema
from app.services.pdf_service import extract_text
from app.services.llm_service import parse_resume_with_llm
from app.services.analysis_service import analyse_resume
from app.services.question_service import generate_questions


async def process_resume(file: UploadFile):
    text = await extract_text(file)

    resume = parse_resume_with_llm(text)
    analysis = analyse_resume(resume)
    questions = generate_questions(resume, analysis)

    return {
        "resume": resume,
        "analysis": analysis,
        "questions": questions,
    }