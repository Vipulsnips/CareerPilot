from fastapi import APIRouter,Depends

from app.schemas.evaluation import AnswerEvaluationRequest,AnswerEvaluation
from app.services.evaluation_service import answer_evaluation
from app.auth import require_auth

router = APIRouter(prefix="/interview", tags=["evaluation"])


@router.post("/evaluate", response_model=AnswerEvaluation)
async def evaluate_answer(request: AnswerEvaluationRequest,auth_state=Depends(require_auth)):
    return answer_evaluation(
        resume=request.resume,
        question=request.question,
        answer=request.answer,
    )
