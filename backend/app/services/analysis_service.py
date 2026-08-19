from ollama import chat
import json
from pydantic import ValidationError
from app.prompts.analysis_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.schemas.analysis import ResumeAnalysis
from app.schemas.resume import ResumeSchema
from app.config.model import LLM_MODEL

def analyse_resume(parsed_resume: ResumeSchema) -> ResumeAnalysis:
    prompt = USER_PROMPT_TEMPLATE.format(text=parsed_resume.model_dump_json())
    response = chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        format="json"
    )
    try:
        data = json.loads(response.message.content)
        analysis = ResumeAnalysis.model_validate(data)
        return analysis
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")
    except ValidationError:
        raise ValueError("LLM response does not match ResumeAnalysis Schema")
