from app.prompts.rag_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.schemas.rag import RAGAnswer
from app.services.gemini_service import generate_structured_response
from app.services.rag.retriever_service import retrieve_documents


def answer_question(
    question: str,
    user_id: str,
) -> RAGAnswer:
    documents = retrieve_documents(
        query=question,
        user_id=user_id,
    )

    context = "\n\n".join(document.page_content for document in documents)

    prompt = USER_PROMPT_TEMPLATE.format(
        context=context,
        question=question,
    )

    return generate_structured_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        response_schema=RAGAnswer,
    )
