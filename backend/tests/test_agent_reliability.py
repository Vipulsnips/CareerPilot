from dotenv import load_dotenv

load_dotenv()

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from app.services import agent_nodes
from app.services.agent_graph import run_agent


def test_agent_stops_after_max_model_calls(monkeypatch):
    model_call_count = 0
    tool_call_count = 0

    class FakeModel:
        def invoke(self, messages):
            nonlocal model_call_count
            model_call_count += 1

            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "search_resume_tool",
                        "args": {"query": "resume"},
                        "id": f"call_{model_call_count}",
                        "type": "tool_call",
                    }
                ],
            )

    def fake_search_resume(**kwargs):
        nonlocal tool_call_count
        tool_call_count += 1
        return []

    monkeypatch.setattr(agent_nodes, "model_with_tools", FakeModel())
    monkeypatch.setattr(agent_nodes, "search_resume", fake_search_resume)

    result = run_agent(
        question="What projects are in my resume?",
        user_id="test_user",
    )

    assert model_call_count == agent_nodes.MAX_MODEL_CALLS
    assert tool_call_count == agent_nodes.MAX_MODEL_CALLS - 1
    assert "couldn't complete" in result.answer.lower()


def test_agent_tool_failure(monkeypatch):
    class FakeModel:
        def invoke(self, messages):
            if any(
                getattr(message, "type", None) == "tool"
                for message in messages
            ):
                return AIMessage(
                    content="I couldn't retrieve your resume information."
                )

            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "search_resume_tool",
                        "args": {"query": "projects"},
                        "id": "call_failure",
                        "type": "tool_call",
                    }
                ],
            )

    def failing_search_resume(**kwargs):
        raise RuntimeError("Chroma database unavailable")

    monkeypatch.setattr(agent_nodes, "model_with_tools", FakeModel())
    monkeypatch.setattr(
        agent_nodes,
        "search_resume",
        failing_search_resume,
    )

    result = run_agent(
        question="What projects are in my resume?",
        user_id="test_user",
    )

    assert result.answer
    assert "couldn't retrieve" in result.answer.lower()


def test_resume_search_uses_authenticated_user_id(monkeypatch):
    captured_calls = []

    def fake_search_resume(**kwargs):
        captured_calls.append(kwargs)
        return [{"content": "User A resume data"}]

    monkeypatch.setattr(
        agent_nodes,
        "search_resume",
        fake_search_resume,
    )

    state = {
        "messages": [
            HumanMessage(content="What projects are in my resume?"),
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "search_resume_tool",
                        "args": {
                            "query": "projects",
                            "user_id": "user_B",
                        },
                        "id": "security_test",
                        "type": "tool_call",
                    }
                ],
            ),
        ],
        "user_id": "user_A",
        "model_calls": 1,
    }

    agent_nodes.run_resume_tool(state)

    assert len(captured_calls) == 1
    assert captured_calls[0]["user_id"] == "user_A"


def test_agent_rejects_unknown_tool():
    state = {
        "messages": [
            HumanMessage(content="Search my resume"),
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "unknown_tool",
                        "args": {},
                        "id": "unknown_call",
                        "type": "tool_call",
                    }
                ],
            ),
        ],
        "user_id": "user_A",
        "model_calls": 1,
    }

    with pytest.raises(ValueError, match="Unknown tool"):
        agent_nodes.run_resume_tool(state)
