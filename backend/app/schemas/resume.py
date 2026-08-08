from pydantic import BaseModel, Field


class Education(BaseModel):
    institution: str | None = None
    degree: str | None = None
    field: str | None = None
    cgpa: float | None = None
    start_year: int | None = None
    end_year: int | None = None


class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None


class Project(BaseModel):
    title: str | None = None
    description: str | None = None
    technologies: list[str] = Field(default_factory=list)


class ResumeSchema(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    github: str | None = None
    linkedin: str | None = None
    summary: str | None = None

    skills: list[str] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
