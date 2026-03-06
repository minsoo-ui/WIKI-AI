"""
LangGraph Builder
=================
Xây dựng và compile Graph hoàn chỉnh cho WIKI-AI.
Supervisor → (route) → Wiki Agent / Respond → END
"""
from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.supervisor import supervisor_node, route_by_intent
from app.graph.wiki_agent import wiki_agent_node
from app.graph.sales_agent import sales_agent_node
from app.graph.summary_agent import summary_agent_node
import logging

logger = logging.getLogger(__name__)

def respond_node(state: AgentState) -> dict:
    intent = state.get("intent", "general")
    query = state.get("user_query", "")

    if intent == "auth":
        response = "Tính năng quản lý tài khoản đang được phát triển. Hiện tại anh/chị có thể sử dụng tài khoản mặc định."
    else:
        response = f"Tôi hiểu câu hỏi của anh/chị: \"{query}\". Xin chào, tôi là WIKI-AI, trợ lý thông tin đa chức năng. Hãy hỏi tôi về kiến thức hoặc sản phẩm nhé!"

    return {"agent_response": response, "agent_used": "supervisor", "return_to_supervisor": False}

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # --- Add Nodes ---
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("wiki_agent", wiki_agent_node)
    graph.add_node("sales_agent", sales_agent_node)
    graph.add_node("summary_agent", summary_agent_node)
    graph.add_node("respond", respond_node)

    # --- Set Entry Point ---
    graph.set_entry_point("supervisor")

    # --- Conditional Edges (Routing) ---
    graph.add_conditional_edges(
        "supervisor",
        route_by_intent,
        {
            "wiki_agent": "wiki_agent",
            "sales_agent": "sales_agent",
            "summary_agent": "summary_agent",
            "respond": "respond",
        },
    )

    # --- Edges to END ---
    graph.add_edge("wiki_agent", END)
    graph.add_edge("sales_agent", END)
    graph.add_edge("summary_agent", END)
    graph.add_edge("respond", END)

    logger.info("[Graph] WIKI-AI Graph compiled successfully with 4 Agents.")
    return graph.compile()

# Singleton compiled graph
_compiled_graph = None

def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph
