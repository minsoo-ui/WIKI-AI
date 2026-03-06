"""
Supervisor Node
===============
Bộ não trung tâm: Phân tích intent bằng Chain-of-Thought và điều hướng.
Chạy trên CPU để dồn GPU cho LLM inference ở Sub-agents.
"""
import re
import logging
from app.graph.state import AgentState

logger = logging.getLogger(__name__)

# Danh sách từ khóa để phân loại intent (Keyword matcher)
INTENT_KEYWORDS = {
    "wiki": ["tìm", "tra cứu", "search", "kiến thức", "wiki", "tài liệu", "hướng dẫn", "là gì"],
    "auth": ["đăng nhập", "đăng xuất", "login", "logout", "tài khoản", "account", "mật khẩu"],
    "summary": ["tóm tắt", "summary", "summarize", "rút gọn", "tổng hợp"],
    "sales": ["mua", "giá", "bao nhiêu tiền", "sản phẩm", "đặt hàng", "order", "bán"],
}

# Câu mô tả các intent để dùng cho Semantic Similarity (Embedding matcher)
INTENT_DESCRIPTIONS = {
    "wiki": "Tra cứu kiến thức chung, tài liệu, hỏi đáp thông tin, tìm hiểu chi tiết",
    "auth": "Quản lý tài khoản, đăng nhập, đăng xuất, đổi mật khẩu",
    "summary": "Tóm tắt một đoạn văn hoặc tài liệu dài thành ngắn gọn",
    "sales": "Hỏi giá cả, mua sắm sản phẩm, đặt hàng, thanh toán",
    "general": "Trò chuyện bình thường, gửi lời chào, cảm ơn, hỏi thăm",
}

def supervisor_node(state: AgentState) -> dict:
    query = state.get("user_query", "").lower().strip()

    if not query:
        return {"intent": "general", "agent_response": "Xin lỗi, tôi không nhận được câu hỏi.", "agent_used": "supervisor", "return_to_supervisor": False}

    intent = _classify_intent_hybrid(query)
    sub_queries = _extract_sub_queries(query)

    logger.info(f"[Supervisor] Query: '{query}' → Intent: {intent}, Sub-queries: {len(sub_queries)}")
    return {"intent": intent, "sub_queries": sub_queries, "return_to_supervisor": True}

def _classify_intent_hybrid(query: str) -> str:
    """Hybrid Routing: 1. Keyword Match -> 2. Embedding Match (Semantic)"""
    # 1. Keyword-based Routing
    scores = {intent: sum(1 for kw in kws if kw in query) for intent, kws in INTENT_KEYWORDS.items()}
    best_intent = max(scores, key=scores.get)

    if scores[best_intent] > 0:
        return best_intent

    # 2. Embedding-based Routing (Semantic Similarity)
    try:
        from app.dependencies import get_embedding
        embedding_service = get_embedding()
        query_vec = embedding_service.embed(query)
        
        # Calculate cosine similarity with intent descriptions
        import numpy as np
        best_semantic_intent = "general"
        highest_sim = -1.0
        
        for intent, desc in INTENT_DESCRIPTIONS.items():
            desc_vec = embedding_service.embed(desc)
            # Dot product since vectors are normalized
            sim = np.dot(query_vec, desc_vec)
            if sim > highest_sim:
                highest_sim = sim
                best_semantic_intent = intent
                
        # Ngưỡng tin cậy (Confidence Threshold)
        if highest_sim > 0.65:
            logger.info(f"[Supervisor] Semantic match: {best_semantic_intent} (Score: {highest_sim:.2f})")
            return best_semantic_intent
            
    except Exception as e:
        logger.error(f"[Supervisor] Semantic routing failed: {e}")

    return "general"

def _extract_sub_queries(query: str) -> list[str]:
    conjunctions = [" và ", " rồi ", " sau đó ", " đồng thời "]
    parts = [query]
    for conj in conjunctions:
        new_parts = []
        for part in parts:
            new_parts.extend(part.split(conj))
        parts = new_parts
    parts = [p.strip() for p in parts if len(p.strip()) > 3]
    return parts if len(parts) > 1 else []

def route_by_intent(state: AgentState) -> str:
    intent = state.get("intent", "general")
    if intent == "wiki":
        return "wiki_agent"
    elif intent == "sales":
        return "sales_agent"
    elif intent == "summary":
        return "summary_agent"
    elif intent == "auth":
        return "respond"
    else:
        return "respond"
