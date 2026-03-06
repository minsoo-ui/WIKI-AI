"""
Graph State Definition
======================
TypedDict cho LangGraph State - Quản lý toàn bộ dữ liệu xuyên suốt Graph.
"""
from typing import TypedDict, Annotated, Optional
from operator import add


class AgentState(TypedDict):
    # Input
    user_query: str
    session_id: str
    user_id: str

    # Memory
    chat_history: list[dict]
    context_summary: str

    # Routing
    intent: str
    sub_queries: list[str]

    # RAG Results
    rag_results: list[dict]
    rag_query_used: str
    rag_crag_retried: bool

    # Output
    agent_response: str
    agent_used: str

    # Control
    return_to_supervisor: bool
    error: Optional[str]

    messages: Annotated[list, add]
