"""
Application Startup & Dependencies
====================================
Khởi tạo các service chính khi ứng dụng FastAPI boot lên.
"""
from app.services.qdrant_service import QdrantService
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.langfuse_service import LangfuseService
from app.rag.pipeline import RAGPipeline
import logging

logger = logging.getLogger(__name__)

# Singleton instances (khởi tạo lazy)
_qdrant: QdrantService = None
_embedding: EmbeddingService = None
_llm: LLMService = None
_rag: RAGPipeline = None
_langfuse: LangfuseService = None


def get_qdrant() -> QdrantService:
    global _qdrant
    if _qdrant is None:
        _qdrant = QdrantService()
    return _qdrant


def get_embedding() -> EmbeddingService:
    global _embedding
    if _embedding is None:
        _embedding = EmbeddingService()
    return _embedding


def get_llm() -> LLMService:
    global _llm
    if _llm is None:
        _llm = LLMService()
    return _llm


def get_langfuse() -> LangfuseService:
    global _langfuse
    if _langfuse is None:
        _langfuse = LangfuseService()
    return _langfuse


def get_rag() -> RAGPipeline:
    global _rag
    if _rag is None:
        qdrant = get_qdrant()
        embedding = get_embedding()
        _rag = RAGPipeline(
            qdrant=qdrant,
            embed_fn=embedding.embed,
        )
    return _rag


def get_system_status() -> dict:
    status = {"services": {}}

    try:
        emb = get_embedding()
        status["services"]["embedding"] = emb.get_status()
    except Exception as e:
        status["services"]["embedding"] = {"ready": False, "error": str(e)}

    try:
        llm = get_llm()
        status["services"]["llm"] = llm.get_status()
    except Exception as e:
        status["services"]["llm"] = {"ready": False, "error": str(e)}

    try:
        qdrant = get_qdrant()
        status["services"]["qdrant"] = qdrant.get_collection_info()
    except Exception as e:
        status["services"]["qdrant"] = {"ready": False, "error": str(e)}

    try:
        lf = get_langfuse()
        status["services"]["langfuse"] = lf.get_status()
    except Exception as e:
        status["services"]["langfuse"] = {"enabled": False, "error": str(e)}

    return status
