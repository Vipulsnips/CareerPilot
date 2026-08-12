from pydantic import BaseModel, Field


class ResumeAnalysis(BaseModel):
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    skill_gaps: list[str] = Field(default_factory=list)
    recommended_topics: list[str] = Field(default_factory=list)
