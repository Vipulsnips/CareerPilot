from google.genai import types


search_resume_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_resume",
            description=(
                "Search the authenticated user's resume for relevant "
                "information. Use this when the answer requires "
                "information from the user's resume. "
                "Use section and item when the question refers to "
                "a specific resume section or item."
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
                    "section": types.Schema(
                        type="STRING",
                        description=(
                            "Optional resume section to restrict the "
                            "search to, such as Projects, Experience, "
                            "Education, or Skills."
                        ),
                    ),
                    "item": types.Schema(
                        type="STRING",
                        description=(
                            "Optional specific item within the section, "
                            "such as a project name or company name."
                        ),
                    ),
                },
                required=["query"],
            ),
        )
    ]
)