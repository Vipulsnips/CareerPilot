from ollama import chat
from app.prompts.resume_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
import json
from pydantic import ValidationError
from app.schemas.resume import ResumeSchema


def parse_resume_with_llm(text: str) -> ResumeSchema:
    prompt = USER_PROMPT_TEMPLATE.format(text=text)
    response = chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    try:
        content = (
            response.message.content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )
        data = json.loads(content)
        resume = ResumeSchema.model_validate(data)
        return resume
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")
    except ValidationError:
        raise ValueError("LLM response does not match ResumeSchema")
