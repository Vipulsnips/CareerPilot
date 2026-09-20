from langchain_chroma import Chroma

from app.services.rag.embedding_service import GeminiEmbeddings


embedding_model = GeminiEmbeddings()

vector_store = Chroma(
    collection_name="careerpilot_resume",
    embedding_function=embedding_model,
    persist_directory="data/chroma",
)
