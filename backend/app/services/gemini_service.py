from typing import TypeVar

from google import genai
from pydantic import BaseModel

from app.config.model import LLM_MODEL

client = genai.Client()

T = TypeVar("T", bound=BaseModel)


def generate_structured_response(
    system_prompt: str,
    user_prompt: str,
    response_schema: type[T],
) -> T:
    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=f"{system_prompt}\n\n{user_prompt}",
        config={
            "response_mime_type": "application/json",
            "response_schema": response_schema,
        },
    )

    return response_schema.model_validate_json(response.text)
