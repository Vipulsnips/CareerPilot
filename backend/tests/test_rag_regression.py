import os

import pytest
from dotenv import load_dotenv

load_dotenv()

from app.services.tools.tool_calling_service import run_tool_calling


TEST_USER_ID = os.getenv("RAG_TEST_USER_ID")


@pytest.mark.skipif(
    not TEST_USER_ID,
    reason="RAG_TEST_USER_ID is not configured",
)
@pytest.mark.parametrize(
    "question,expected",
    [
        (
            "What technologies did I use in my CareerPilot project?",
            ["FastAPI"],
        ),
        (
            "What technologies did I use in APIShield?",
            ["APIShield"],
        ),
        (
            "What technologies did I use in the Delhi Metro Route Planner?",
            ["Streamlit"],
        ),
        (
            "What projects are in my resume?",
            ["CareerPilot", "APIShield", "Delhi Metro"],
        ),
        (
            "Where did I study and what are my educational qualifications?",
            ["B.Tech", "GL Bajaj"],
        ),
        (
            "What is the capital of France?",
            ["resume-related"],
        ),
        (
            "How did I use Redis in my projects?",
            ["Redis"],
        ),
        (
            "What technologies did I use across my projects?",
            ["FastAPI", "Streamlit"],
        ),
    ],
)
def test_rag_regression(question: str, expected: list[str]):
    result = run_tool_calling(
        question=question,
        user_id=TEST_USER_ID,
    )

    assert result.answer
    assert result.answer.strip()

    answer = result.answer.lower()

    for expected_value in expected:
        assert expected_value.lower() in answer