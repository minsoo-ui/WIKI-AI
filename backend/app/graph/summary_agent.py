"""
Summary Agent Node
==================
Sub-agent chuyên tóm tắt các tài liệu, đoạn chat dài.
"""
import logging
from app.graph.state import AgentState

logger = logging.getLogger(__name__)

def summary_agent_node(state: AgentState) -> dict:
    """
    Xử lý các yêu cầu tóm tắt.
    """
    query = state.get("user_query", "")
    rag_results = state.get("rag_results", [])
    
    if rag_results:
        # Nếu có kết quả RAG, tóm tắt nội dung đó
        text_to_summarize = " ".join([res.get("text", "") for res in rag_results[:2]])
        # TODO: Cần chuyển logic này cho LLM xử lý
        response = f"📝 **Bản tóm tắt tự động:**\n{text_to_summarize[:150]}...\n\n(Chức năng tóm tắt AI đang được hoàn thiện)"
    else:
        response = "Bạn muốn tôi tóm tắt nội dung nào? Hãy cung cấp thêm thông tin hoặc tài liệu nhé."

    return {
        "agent_response": response,
        "agent_used": "summary_agent",
        "return_to_supervisor": True,
    }
