from app.services.rag.retriever_service import (
    retrieve_documents,
    retrieve_section_documents,
)


def search_resume(
    query: str,
    user_id: str,
    section: str | None = None,
    item: str | None = None,
) -> list[dict[str, str]]:

    if section and not item:
        documents = retrieve_section_documents(
            user_id=user_id,
            section=section,
        )
    else:
        documents = retrieve_documents(
            query=query,
            user_id=user_id,
            section=section,
            item=item,
        )

    # If a section/item filter returned nothing,
    # retry with user-scoped semantic search.
    if not documents and (section or item):
        documents = retrieve_documents(
            query=query,
            user_id=user_id,
        )

    return [
        {
            "content": document.page_content,
            "section": document.metadata.get("section", ""),
            "item": document.metadata.get("item", ""),
        }
        for document in documents
    ]