from fastapi import APIRouter

from app.schemas.interviewConfig import InterviewStartRequest
from app.schemas.questions import InterviewQuestions
from app.services.question_service import generate_questions


router = APIRouter(prefix="/interview", tags=["interview"])


@router.post("/start", response_model=InterviewQuestions)
async def start_interview(request: InterviewStartRequest):
    return generate_questions(
        resume=request.resume,
        analysis=request.analysis,
        config=request.config,
    )