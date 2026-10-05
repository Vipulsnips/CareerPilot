from langchain_core.documents import Document

from app.schemas.resume import ResumeSchema
from app.services.rag.text_splitter_service import split_documents
from app.services.rag.vector_store_service import vector_store


def _build_documents(
    resume: ResumeSchema,
    user_id: str,
) -> list[Document]:

    documents: list[Document] = []

    def add(
        content: str,
        section: str,
        item: str = "",
    ) -> None:

        if not content.strip():
            return

        documents.append(
            Document(
                page_content=content.strip(),
                metadata={
                    "user_id": user_id,
                    "source": "resume",
                    "section": section,
                    "item": item,
                },
            )
        )

    if resume.summary:
        add(
            content=f"Summary\n\n{resume.summary}",
            section="Summary",
        )

    if resume.skills:
        add(
            content=f"Skills\n\n{', '.join(resume.skills)}",
            section="Skills",
        )

    for project in resume.projects:
        content = (
            f"Project: {project.title}\n\n"
            f"{project.description}\n"
            f"Technologies: {', '.join(project.technologies)}"
        )

        add(
            content=content,
            section="Projects",
            item=project.title or "",
        )

    for experience in resume.experience:
        content = (
            f"Experience: {experience.role} "
            f"at {experience.company} "
            f"({experience.duration})\n\n"
            f"{experience.description}"
        )

        add(
            content=content,
            section="Experience",
            item=experience.company or "",
        )

    for education in resume.education:
        content = (
            f"Education: {education.degree} "
            f"in {education.field}, "
            f"{education.institution} "
            f"({education.start_year}-{education.end_year})"
        )

        add(
            content=content,
            section="Education",
            item=education.institution or "",
        )

    return documents


def index_resume(
    resume: ResumeSchema,
    user_id: str,
) -> None:

    vector_store.delete(
        where={
            "$and": [
                {"user_id": user_id},
                {"source": "resume"},
            ]
        }
    )

    documents = _build_documents(
        resume=resume,
        user_id=user_id,
    )

    chunks = split_documents(documents)

    vector_store.add_documents(chunks)