from ollama import chat
from app.prompts.evaluation_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
import json
from pydantic import ValidationError
from app.schemas.evaluation import AnswerEvaluation
from app.schemas.resume import ResumeSchema
from app.schemas.questions import InterviewQuestion
from app.config.model import LLM_MODEL

def answer_evaluation(resume:ResumeSchema,question:InterviewQuestion,answer:str)->AnswerEvaluation:
  prompt=USER_PROMPT_TEMPLATE.format(resume=resume.model_dump_json(),question=question.model_dump_json(),answer=answer)
  response=chat(
    model=LLM_MODEL,
    messages=[
      {"role": "system","content":SYSTEM_PROMPT},
      {"role": "user","content":prompt}
    ])  
  try:
      content = (
          response.message.content
          .replace("```json", "")
          .replace("```", "")
          .strip()
      )
      data = json.loads(content)
      evaluation = AnswerEvaluation.model_validate(data)
      return evaluation
  except json.JSONDecodeError:
      raise ValueError("LLM returned invalid JSON")
  except ValidationError:
      raise ValueError("LLM response does not matchAnswerEvaluation schema")