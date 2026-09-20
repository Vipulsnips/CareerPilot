from pydantic import BaseModel


class RAGAnswer(BaseModel):
    answer: str