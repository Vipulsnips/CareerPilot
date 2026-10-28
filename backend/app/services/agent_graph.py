from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from app.schemas.rag import RAGAnswer
from app.services.agent_nodes import (
    call_model,
    finish_on_limit,
    route_after_model,
    run_resume_tool,
)
from app.services.agent_state import AgentState


builder = StateGraph(AgentState)

builder.add_node("call_model", call_model)
builder.add_node("run_resume_tool", run_resume_tool)
builder.add_node("finish_on_limit", finish_on_limit)

builder.add_edge(START, "call_model")

builder.add_conditional_edges(
    "call_model",
    route_after_model,
    {
        "run_resume_tool": "run_resume_tool",
        "max_calls_reached": "finish_on_limit",
        "END": END,
    },
)

builder.add_edge("run_resume_tool", "call_model")
builder.add_edge("finish_on_limit", END)

agent_graph = builder.compile()


def run_agent(question: str, user_id: str) -> RAGAnswer:
    result = agent_graph.invoke(
        {
            "messages": [HumanMessage(content=question)],
            "user_id": user_id,
            "model_calls": 0,
        }
    )

    content = result["messages"][-1].content

    if not isinstance(content, str):
        content = "".join(
            block.get("text", "") for block in content if isinstance(block, dict)
        )

    return RAGAnswer(
        answer=content or "I couldn't generate an answer for that question."
    )
