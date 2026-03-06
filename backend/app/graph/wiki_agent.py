"""
Wiki Agent Node
===============
Sub-agent chuyên truy vấn WIKI thông qua Advanced RAG Pipeline.
"""
import logging
from app.graph.state import AgentState

logger = logging.getLogger(__name__)

def wiki_agent_node(state: AgentState) -> dict:
    query = state.get("user_query", "")
    rag_results = state.get("rag_results", [])

    if rag_results:
        response = _format_rag_response(query, rag_results)
    else:
        response = f"Tôi đã tìm kiếm trong kho kiến thức WIKI nhưng chưa tìm thấy thông tin về \"{query}\"."

    return {
        "agent_response": response,
        "agent_used": "wiki_agent",
        "return_to_supervisor": True,
    }

def _format_rag_response(query: str, results: list[dict]) -> str:
    if not results:
        return f"Không tìm thấy kết quả cho \"{query}\"."
    parts = [f"📚 **Kết quả Wiki cho \"{query}\":**\n"]
    for i, result in enumerate(results[:3], 1):
        text = result.get("text", "")[:300]
        score = result.get("final_score", result.get("score", 0))
        source = result.get("source", "unknown")
        parts.append(f"**{i}. [{source}]** _({score:.2f})_\n{text}\n")
    return "\n".join(parts)
