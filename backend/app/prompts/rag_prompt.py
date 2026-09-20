SYSTEM_PROMPT = """
You answer questions using only the provided context.

If the context does not contain enough information to answer the question,
say that the information is not available in the provided context.
"""


USER_PROMPT_TEMPLATE = """
Context:
{context}

Question:
{question}
"""