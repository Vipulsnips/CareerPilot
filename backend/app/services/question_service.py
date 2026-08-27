from pydantic import ValidationError

from app.schemas.resume import ResumeSchema
from app.schemas.analysis import ResumeAnalysis
from app.schemas.questions import InterviewQuestions
from app.schemas.interviewConfig import InterviewConfig
from app.prompts.question_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.services.gemini_service import generate_structured_response


def generate_questions(
    resume: ResumeSchema,
    analysis: ResumeAnalysis,
    config: InterviewConfig,
) -> InterviewQuestions:
    skills = config.skills or resume.skills

    prompt = USER_PROMPT_TEMPLATE.format(
        resume=resume.model_dump_json(),
        analysis=analysis.model_dump_json(),
        question_count=config.question_count,
        skills=",".join(skills),
    )

    try:
        return generate_structured_response(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            response_schema=InterviewQuestions,
        )
    except ValidationError:
        raise ValueError("LLM response does not match InterviewQuestions Schema")
