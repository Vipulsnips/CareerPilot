from langchain_core.documents import Document

from app.services.rag.vector_store_service import vector_store


def retrieve_documents(
    query: str,
    user_id: str,
) -> list[Document]:
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 2,
            "filter": {"user_id": user_id},
        },
    )

    return retriever.invoke(query)