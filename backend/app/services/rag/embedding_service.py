from google import genai
from langchain_core.embeddings import Embeddings


EMBEDDING_MODEL = "gemini-embedding-001"

client = genai.Client()


def generate_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values


class GeminiEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [generate_embedding(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return generate_embedding(text)
