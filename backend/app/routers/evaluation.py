from fastapi import APIRouter

from app.schemas.evaluation import AnswerEvaluationRequest,AnswerEvaluation
from app.services.evaluation_service import answer_evaluation

router = APIRouter(prefix="/interview", tags=["evaluation"])


@router.post("/evaluate", response_model=AnswerEvaluation)
async def evaluate_answer(request: AnswerEvaluationRequest):
    return answer_evaluation(
        resume=request.resume,
        question=request.question,
        answer=request.answer,
    )
