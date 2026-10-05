from langchain_core.documents import Document

from app.services.rag.vector_store_service import vector_store


def retrieve_documents(
    query: str,
    user_id: str,
    section: str | None = None,
    item: str | None = None,
) -> list[Document]:
    filters = [
        {"user_id": user_id},
    ]
    if section:
        filters.append({"section": section})
    if item:
        filters.append({"item": item})
    if len(filters) == 1:
        metadata_filter = filters[0]
    else:
        metadata_filter = {
            "$and": filters,
        }
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "fetch_k": 20,
            "lambda_mult": 0.5,
            "filter": metadata_filter,
        },
    )

    documents = retriever.invoke(query)

    unique_documents = []
    seen_content = set()

    for document in documents:
        if document.page_content in seen_content:
            continue

        seen_content.add(document.page_content)
        unique_documents.append(document)

    return unique_documents