from app.prompts.resume_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.schemas.resume import ResumeSchema
from app.services.gemini_service import generate_structured_response


def parse_resume_with_llm(text: str) -> ResumeSchema:
    prompt = USER_PROMPT_TEMPLATE.format(text=text)
    return generate_structured_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        response_schema=ResumeSchema,
    )
