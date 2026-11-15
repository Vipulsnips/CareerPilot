from dotenv import load_dotenv

load_dotenv()

from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document

from app.services.rag import retriever_service


class FakeEmbeddings(Embeddings):
    """Deterministic embeddings for isolated Chroma tests."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0, 0.0] for _ in texts]

    def embed_query(self, text: str) -> list[float]:
        return [1.0, 0.0, 0.0]


def test_chroma_enforces_user_level_isolation(monkeypatch, tmp_path):
    # Create a temporary Chroma collection.
    test_store = Chroma(
        collection_name="isolation_test",
        embedding_function=FakeEmbeddings(),
        persist_directory=str(tmp_path),
    )

    # Insert both users' documents into the SAME collection.
    test_store.add_documents(
        documents=[
            Document(
                page_content="User A worked on Project Falcon using FastAPI.",
                metadata={
                    "user_id": "user_A",
                    "source": "resume",
                    "section": "Projects",
                    "item": "Project Falcon",
                },
            ),
            Document(
                page_content="User B worked on Project Orion using Django.",
                metadata={
                    "user_id": "user_B",
                    "source": "resume",
                    "section": "Projects",
                    "item": "Project Orion",
                },
            ),
        ],
        ids=["user-a-project", "user-b-project"],
    )

    # Make the actual retrieval functions use our temporary collection.
    monkeypatch.setattr(
        retriever_service,
        "vector_store",
        test_store,
    )

    # Test semantic retrieval for both users.
    user_a_results = retriever_service.retrieve_documents(
        query="Tell me about projects",
        user_id="user_A",
    )

    user_b_results = retriever_service.retrieve_documents(
        query="Tell me about projects",
        user_id="user_B",
    )

    assert len(user_a_results) == 1
    assert "Project Falcon" in user_a_results[0].page_content
    assert all(
        "Project Orion" not in doc.page_content
        for doc in user_a_results
    )

    assert len(user_b_results) == 1
    assert "Project Orion" in user_b_results[0].page_content
    assert all(
        "Project Falcon" not in doc.page_content
        for doc in user_b_results
    )

    # Test section retrieval for both users.
    user_a_section = retriever_service.retrieve_section_documents(
        user_id="user_A",
        section="Projects",
    )

    user_b_section = retriever_service.retrieve_section_documents(
        user_id="user_B",
        section="Projects",
    )

    assert len(user_a_section) == 1
    assert "Project Falcon" in user_a_section[0].page_content

    assert len(user_b_section) == 1
    assert "Project Orion" in user_b_section[0].page_content
