from app.prompts.evaluation_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.schemas.evaluation import AnswerEvaluation
from app.schemas.resume import ResumeSchema
from app.schemas.questions import InterviewQuestion
from app.services.gemini_service import generate_structured_response
from app.logging_config import logger


def answer_evaluation(
    resume: ResumeSchema,
    question: InterviewQuestion,
    answer: str,
) -> AnswerEvaluation:
    logger.info(
        "Answer evaluation started",
        extra={"event": "answer_evaluation_started"},
    )

    prompt = USER_PROMPT_TEMPLATE.format(
        resume=resume.model_dump_json(),
        question=question.model_dump_json(),
        answer=answer,
    )

    result = generate_structured_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        response_schema=AnswerEvaluation,
    )

    logger.info(
        "Answer evaluation completed",
        extra={"event": "answer_evaluation_completed"},
    )

    return result
