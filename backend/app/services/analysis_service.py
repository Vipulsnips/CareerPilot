from app.prompts.analysis_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.schemas.analysis import ResumeAnalysis
from app.schemas.resume import ResumeSchema
from app.services.gemini_service import generate_structured_response


def analyse_resume(parsed_resume: ResumeSchema) -> ResumeAnalysis:
    prompt = USER_PROMPT_TEMPLATE.format(text=parsed_resume.model_dump_json())
    return generate_structured_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        response_schema=ResumeAnalysis,
    )
