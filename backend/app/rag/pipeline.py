"""
Advanced RAG Pipeline
=====================
Quy trình RAG 3 Layer: Query Expansion → Vector Search + Reranking → CRAG.
"""
from typing import Optional
from app.services.qdrant_service import QdrantService
from app.rag.query_expansion import expand_query
from app.rag.reranker import rerank_results
import logging

logger = logging.getLogger(__name__)

CRAG_SCORE_THRESHOLD = 0.3

class RAGPipeline:
    def __init__(self, qdrant: QdrantService, embed_fn):
        self.qdrant = qdrant
        self.embed_fn = embed_fn

    def retrieve(self, query: str, top_k: int = 5, category: Optional[str] = None) -> dict:
        # L1: Query Expansion
        expanded_query, expanded_keywords = expand_query(query)
        query_vector = self.embed_fn(expanded_query)

        # L2: Vector Search & Reranking
        raw_results = self.qdrant.search(query_vector=query_vector, top_k=top_k * 2, category_filter=category)
        if not raw_results:
            return self._empty_result(expanded_query, False)

        reranked = rerank_results(raw_results, query, expanded_keywords)
        top_results = reranked[:top_k]

        # L3: CRAG Retry
        best_score = top_results[0]["final_score"] if top_results else 0
        if best_score < CRAG_SCORE_THRESHOLD:
            logger.info(f"[CRAG] Retry triggered. Score {best_score} < {CRAG_SCORE_THRESHOLD}")
            return self._crag_retry(query, top_k, category)

        return {"results": top_results, "query_used": expanded_query, "crag_retried": False, "total_found": len(top_results)}

    def _crag_retry(self, original_query: str, top_k: int, category: Optional[str]) -> dict:
        noise_words = ["tốt nhất", "rẻ nhất", "bán chạy", "phổ biến", "giá rẻ", "chất lượng", "tốt", "rẻ", "hay", "đánh giá", "review"]
        simplified = original_query.lower()
        for word in noise_words:
            simplified = simplified.replace(word, "").strip()
        simplified = " ".join(simplified.split())

        if not simplified or simplified == original_query.lower():
            return self._empty_result(original_query, True)

        query_vector = self.embed_fn(simplified)
        raw_results = self.qdrant.search(query_vector=query_vector, top_k=top_k * 2, category_filter=category)
        if not raw_results:
            return self._empty_result(simplified, True)

        reranked = rerank_results(raw_results, simplified, [])
        return {"results": reranked[:top_k], "query_used": simplified, "crag_retried": True, "total_found": len(reranked[:top_k])}

    @staticmethod
    def _empty_result(query: str, crag_retried: bool) -> dict:
        return {"results": [], "query_used": query, "crag_retried": crag_retried, "total_found": 0}
