from google.genai import types


search_resume_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_resume",
            description=(
                "Search the authenticated user's resume for relevant "
                "information. Use this when the answer requires "
                "information from the user's resume."
            ),
            parameters=types.Schema(
                type="OBJECT",
                properties={
                    "query": types.Schema(
                        type="STRING",
                        description=(
                            "A concise search query describing the "
                            "resume information needed."
                        ),
                    ),
                },
                required=["query"],
            ),
        )
    ]
)