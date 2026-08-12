import json
from ollama import chat
from app.schemas.resume import ResumeSchema
from app.schemas.analysis import ResumeAnalysis
from app.schemas.questions import InterviewQuestions
from app.schemas.interviewConfig import InterviewConfig
from app.prompts.question_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from pydantic import ValidationError
from app.config.model import LLM_MODEL

def generate_questions(resume: ResumeSchema, analysis: ResumeAnalysis, config:InterviewConfig) -> InterviewQuestions:
    skills = config.skills or resume.skills
    prompt = USER_PROMPT_TEMPLATE.format(resume=resume.model_dump_json(), analysis=analysis.model_dump_json(),question_count=config.question_count,skills=",".join(skills))
    response = chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    try:
        content = (
            response.message.content.replace("```json", "").replace("```", "").strip()
        )
        data = json.loads(content)
        questions = InterviewQuestions.model_validate(data)
        return questions
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")
    except ValidationError:
        raise ValueError("LLM response does not match InterviewQuestions Schema")
