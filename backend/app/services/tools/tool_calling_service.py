from google.genai import types

from app.config.model import LLM_MODEL
from app.schemas.rag import RAGAnswer
from app.services.gemini_service import client
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

    max_iterations = 3

    for _ in range(max_iterations):

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
                answer=response.text
                or "I couldn't generate an answer for that question."
            )

        contents.append(
            response.candidates[0].content
        )

        function_response_parts = []

        for function_call in function_calls:

            if function_call.name != "search_resume":
                raise ValueError(
                    f"Unknown tool: {function_call.name}"
                )
            query = function_call.args["query"]
            section = function_call.args.get("section")
            item = function_call.args.get("item")

            documents = search_resume(
                query=query,
                user_id=user_id,
                section=section,
                item=item,
            )

            function_response = types.FunctionResponse(
                name=function_call.name,
                response={
                    "result": documents,
                },
                id=function_call.id,
            )

            function_response_parts.append(
                types.Part(
                    function_response=function_response,
                )
            )

        contents.append(
            types.Content(
                role="user",
                parts=function_response_parts,
            )
        )

    return RAGAnswer(
        answer=(
            "I couldn't gather enough information "
            "from your resume to answer that."
        )
    )