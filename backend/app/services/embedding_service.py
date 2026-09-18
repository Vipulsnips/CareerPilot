from dotenv import load_dotenv
from google import genai

load_dotenv()

EMBEDDING_MODEL = "gemini-embedding-001"

client = genai.Client()


def generate_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values