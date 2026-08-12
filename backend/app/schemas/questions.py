from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):
    question: str
    category: str
    difficulty: str


class InterviewQuestions(BaseModel):
    questions: list[InterviewQuestion] = Field(default_factory=list)