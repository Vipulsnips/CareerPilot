from pydantic import BaseModel, Field

from app.schemas.resume import ResumeSchema
from app.schemas.analysis import ResumeAnalysis


class InterviewConfig(BaseModel):
    skills: list[str] = Field(default_factory=list)
    question_count: int = Field(default=10, ge=1, le=20)


class InterviewStartRequest(BaseModel):
    resume: ResumeSchema
    analysis: ResumeAnalysis
    config: InterviewConfig