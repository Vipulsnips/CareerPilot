from app.prompts.analysis_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.schemas.analysis import ResumeAnalysis
from app.schemas.resume import ResumeSchema
from app.services.gemini_service import generate_structured_response
from app.logging_config import logger


def analyse_resume(parsed_resume: ResumeSchema) -> ResumeAnalysis:
    logger.info(
        "Resume analysis started",
        extra={"event": "resume_analysis_started"},
    )

    prompt = USER_PROMPT_TEMPLATE.format(text=parsed_resume.model_dump_json())

    result = generate_structured_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        response_schema=ResumeAnalysis,
    )

    logger.info(
        "Resume analysis completed",
        extra={"event": "resume_analysis_completed"},
    )

    return result
