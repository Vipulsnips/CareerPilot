from fastapi import APIRouter, Depends

from app.auth import require_auth
from app.schemas.rag import RAGAnswer
from app.schemas.rag_request import RAGQuestionRequest
from app.services.rag.rag_service import answer_question


router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/ask", response_model=RAGAnswer)
async def ask_question(
    request: RAGQuestionRequest,
    auth_state=Depends(require_auth),
):
    user_id = auth_state.payload["sub"]

    return answer_question(
        question=request.question,
        user_id=user_id,
    )