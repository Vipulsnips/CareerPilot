from app.services.rag.retriever_service import retrieve_documents


def search_resume(
    query: str,
    user_id: str,
    section: str | None = None,
    item: str | None = None,
) -> list[dict[str, str]]:

    documents = retrieve_documents(
        query=query,
        user_id=user_id,
        section=section,
        item=item,
    )

    return [
        {
            "content": document.page_content,
            "section": document.metadata.get("section", ""),
        }
        for document in documents
    ]