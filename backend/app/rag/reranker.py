"""
Layer 2: Custom Reranking (Code-only)
=====================================
Chấm điểm kết quả tìm kiếm bằng logic thuần, KHÔNG dùng AI.
Tiết kiệm tối đa tài nguyên GPU cho LLM inference.

Scoring System (từ BRIEF.md):
  - Khớp chính xác tên/mã sản phẩm: +3.0 điểm
  - Keyword Match:                   +1.0 điểm
  - Category Match:                  +0.5 điểm
"""
import re


def rerank_results(
    results: list[dict],
    original_query: str,
    expanded_keywords: list[str],
) -> list[dict]:
    """
    Chấm điểm và sắp xếp lại kết quả tìm kiếm.

    Args:
        results: Kết quả từ Qdrant [{text, score, category, source, doc_id}].
        original_query: Query gốc từ người dùng.
        expanded_keywords: Từ khóa mở rộng từ Layer 1.

    Returns:
        Danh sách đã sắp xếp, mỗi item thêm trường "rerank_score" và "final_score".
    """
    query_lower = original_query.lower().strip()
    query_words = set(re.findall(r'\w+', query_lower))

    scored_results = []

    for result in results:
        text_lower = result.get("text", "").lower()
        rerank_score = 0.0

        # === Rule 1: Khớp chính xác tên/mã (+3.0) ===
        if query_lower in text_lower:
            rerank_score += 3.0

        # === Rule 2: Keyword Match (+1.0 mỗi từ khớp) ===
        text_words = set(re.findall(r'\w+', text_lower))
        matched_words = query_words.intersection(text_words)
        rerank_score += len(matched_words) * 1.0

        # Bonus cho expanded keywords match
        for kw in expanded_keywords:
            if kw.lower() in text_lower:
                rerank_score += 0.5

        # === Rule 3: Category Match (+0.5) ===
        category = result.get("category", "").lower()
        for word in query_words:
            if word in category:
                rerank_score += 0.5
                break

        # Final score = vector similarity * 0.4 + rerank_score * 0.6
        vector_score = result.get("score", 0)
        final_score = (vector_score * 0.4) + (rerank_score / max(rerank_score, 1) * 0.6)

        scored_results.append({
            **result,
            "rerank_score": round(rerank_score, 2),
            "vector_score": round(vector_score, 4),
            "final_score": round(final_score, 4),
        })

    # Sắp xếp theo final_score giảm dần
    scored_results.sort(key=lambda x: x["final_score"], reverse=True)
    return scored_results
