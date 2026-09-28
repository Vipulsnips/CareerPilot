from google.genai import types

from app.config.model import LLM_MODEL
from app.prompts.rag_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.schemas.rag import RAGAnswer
from app.services.gemini_service import client, generate_structured_response
from app.services.tools.resume_tools import search_resume
from app.services.tools.tool_definitions import search_resume_tool


TOOL_CALLING_SYSTEM_PROMPT = """
You are the resume assistant for CareerPilot.

Decide whether the user's question requires information from their
resume.

If it does, call search_resume with a short, self-contained query.

If it does not relate to the user's resume, do not call the tool and
say that you can only help with resume-related questions.

Do not guess or invent information.
"""


def run_tool_calling(
    question: str,
    user_id: str,
) -> RAGAnswer:

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=question),
            ],
        )
    ]

    config = types.GenerateContentConfig(
        system_instruction=TOOL_CALLING_SYSTEM_PROMPT,
        tools=[search_resume_tool],
    )

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=contents,
        config=config,
    )

    function_calls = [
        part.function_call
        for part in response.candidates[0].content.parts
        if part.function_call
    ]

    if not function_calls:
        return RAGAnswer(
            answer=response.text or "I couldn't generate an answer for that question."
        )

    function_call = function_calls[0]

    if function_call.name != "search_resume":
        raise ValueError(f"Unknown tool: {function_call.name}")

    query = function_call.args["query"]

    documents = search_resume(
        query=query,
        user_id=user_id,
    )

    context = "\n\n".join(document["content"] for document in documents)

    prompt = USER_PROMPT_TEMPLATE.format(
        context=context,
        question=question,
    )

    return generate_structured_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        response_schema=RAGAnswer,
    )
