from langchain_core.documents import Document

from app.services.rag.text_splitter_service import split_documents
from app.services.rag.vector_store_service import vector_store


def index_resume(
    text: str,
    user_id: str,
) -> None:
    document = Document(
        page_content=text,
        metadata={
            "source": "resume",
            "user_id": user_id,
        },
    )

    chunks = split_documents([document])

    vector_store.add_documents(chunks)
