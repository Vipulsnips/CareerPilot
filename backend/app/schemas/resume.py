from pydantic import BaseModel,Field

class ResumeSchema(BaseModel):
  name: str | None = None
  email: str | None = None
  phone: str | None = None
  github: str | None = None
  linkedin: str | None = None
  summary: str | None = None

  skills: list[str] =Field(default_factory=list)
  education: list[str] =Field(default_factory=list)
  experience: list[str] =Field(default_factory=list)
  projects: list[str] =Field(default_factory=list)
  certifications: list[str] =Field(default_factory=list)