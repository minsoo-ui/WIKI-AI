"""
Qdrant Vector Database Service
==============================
Quản lý kết nối, indexing và tìm kiếm vector.
Hỗ trợ 2 chế độ: Local (memmap) và Server (Docker).
"""
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from typing import Optional
from app.config import get_settings
import uuid
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class QdrantService:
    """Quản lý toàn bộ thao tác với Qdrant Vector DB."""

    def __init__(self):
        """Khởi tạo kết nối Qdrant (local hoặc server)."""
        if settings.QDRANT_USE_LOCAL:
            # Chế độ Local: lưu thẳng trên ổ cứng (memmap)
            self.client = QdrantClient(path=settings.QDRANT_LOCAL_PATH)
            logger.info(f"Qdrant Local mode: {settings.QDRANT_LOCAL_PATH}")
        else:
            # Chế độ Server: kết nối qua Docker
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
            )
            logger.info(f"Qdrant Server: {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")

        self._ensure_collection()

    def _ensure_collection(self):
        """Tạo collection nếu chưa tồn tại."""
        collections = [c.name for c in self.client.get_collections().collections]
        if settings.QDRANT_COLLECTION not in collections:
            self.client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIMENSION,
                    distance=Distance.COSINE,
                    on_disk=True,  # Memmap storage - tối ưu RAM
                ),
            )
            logger.info(f"Created collection: {settings.QDRANT_COLLECTION}")

    def upsert_documents(self, documents: list[dict], vectors: list[list[float]]):
        """
        Đưa tài liệu vào Qdrant.

        Args:
            documents: List of {"text": ..., "metadata": {"category": ..., "source": ...}}
            vectors: List of embedding vectors tương ứng.
        """
        points = []
        for doc, vector in zip(documents, vectors):
            point_id = str(uuid.uuid4())
            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "text": doc["text"],
                        "category": doc.get("metadata", {}).get("category", "general"),
                        "source": doc.get("metadata", {}).get("source", "unknown"),
                        "doc_id": doc.get("metadata", {}).get("doc_id", point_id),
                    },
                )
            )

        self.client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points,
        )
        logger.info(f"Upserted {len(points)} documents to Qdrant.")

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        category_filter: Optional[str] = None,
        score_threshold: float = 0.0,
    ) -> list[dict]:
        """
        Tìm kiếm vector trong Qdrant.

        Args:
            query_vector: Embedding vector của câu truy vấn.
            top_k: Số kết quả trả về.
            category_filter: Lọc theo danh mục (nếu có).
            score_threshold: Ngưỡng điểm tối thiểu.

        Returns:
            List of {"text", "score", "category", "source", "doc_id"}
        """
        search_filter = None
        if category_filter:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category_filter),
                    )
                ]
            )

        results = self.client.search(
            collection_name=settings.QDRANT_COLLECTION,
            query_vector=query_vector,
            limit=top_k,
            query_filter=search_filter,
            score_threshold=score_threshold,
        )

        return [
            {
                "text": hit.payload.get("text", ""),
                "score": hit.score,
                "category": hit.payload.get("category", ""),
                "source": hit.payload.get("source", ""),
                "doc_id": hit.payload.get("doc_id", ""),
            }
            for hit in results
        ]

    def get_collection_info(self) -> dict:
        """Lấy thông tin collection hiện tại."""
        info = self.client.get_collection(settings.QDRANT_COLLECTION)
        return {
            "name": settings.QDRANT_COLLECTION,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": info.status.value,
        }
