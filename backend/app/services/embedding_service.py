"""
Embedding Service
=================
Tạo text embeddings bằng nomic-embed-text-v1.5 (768 dimensions).
Sử dụng sentence-transformers hoặc fallback sang Ollama embeddings.
"""
import logging
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EmbeddingService:
    """
    Embedding service cho WIKI-AI.
    Model mặc định: nomic-embed-text-v1.5 (768 dimensions).
    """

    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION
        self._model = None
        self._init_model()

    def _init_model(self):
        """Khởi tạo embedding model."""
        try:
            from sentence_transformers import SentenceTransformer

            logger.info(f"[Embedding] Loading: {self.model_name}")
            self._model = SentenceTransformer(
                self.model_name,
                trust_remote_code=True,
            )
            logger.info(f"[Embedding] Loaded. Dimension: {self.dimension}")

        except ImportError:
            logger.warning(
                "[Embedding] sentence-transformers not installed. "
                "Trying Ollama embeddings fallback."
            )
            self._model = None

        except Exception as e:
            logger.error(f"[Embedding] Failed to load model: {e}")
            self._model = None

    def embed(self, text: str) -> list[float]:
        """
        Tạo embedding vector cho một đoạn text.

        Args:
            text: Văn bản cần embedding.

        Returns:
            Vector list[float] với dimension = 768.
        """
        if self._model is not None:
            return self._embed_local(text)
        else:
            return self._embed_ollama(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Tạo embedding cho nhiều đoạn text cùng lúc.
        Hiệu quả hơn gọi embed() từng cái.
        """
        if self._model is not None:
            return self._embed_local_batch(texts)
        else:
            return [self._embed_ollama(t) for t in texts]

    def _embed_local(self, text: str) -> list[float]:
        """Embedding bằng sentence-transformers (local)."""
        # nomic-embed yêu cầu prefix "search_query:" hoặc "search_document:"
        prefixed = f"search_query: {text}"
        vector = self._model.encode(prefixed, normalize_embeddings=True)
        return vector.tolist()

    def _embed_local_batch(self, texts: list[str]) -> list[list[float]]:
        """Batch embedding local."""
        prefixed = [f"search_document: {t}" for t in texts]
        vectors = self._model.encode(prefixed, normalize_embeddings=True, batch_size=32)
        return vectors.tolist()

    def _embed_ollama(self, text: str) -> list[float]:
        """Fallback: embedding qua Ollama API."""
        try:
            import httpx

            response = httpx.post(
                "http://localhost:11434/api/embeddings",
                json={
                    "model": "nomic-embed-text",
                    "prompt": text,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json().get("embedding", [0.0] * self.dimension)

        except Exception as e:
            logger.error(f"[Embedding] Ollama fallback failed: {e}")
            # Zero vector fallback (sẽ không match bất kỳ kết quả nào)
            return [0.0] * self.dimension

    def get_status(self) -> dict:
        """Trạng thái embedding service."""
        return {
            "model": self.model_name,
            "dimension": self.dimension,
            "ready": self._model is not None,
            "backend": "sentence-transformers" if self._model else "ollama-fallback",
        }
