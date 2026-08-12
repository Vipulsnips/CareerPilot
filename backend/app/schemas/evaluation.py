from pydantic import BaseModel, Field

from app.schemas.questions import InterviewQuestion
from app.schemas.resume import ResumeSchema


class AnswerEvaluation(BaseModel):
    score: int
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    feedback: str


class AnswerEvaluationRequest(BaseModel):
    resume: ResumeSchema
    question: InterviewQuestion
    answer: str