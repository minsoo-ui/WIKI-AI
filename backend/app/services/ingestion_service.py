"""
Data Ingestion Service
======================
Đọc raw data từ thư mục assets/ và đưa vào Qdrant Vector DB.
Hỗ trợ: JSON, Markdown, Plain Text.
"""
import json
import os
import logging
from pathlib import Path
from typing import Optional
from app.services.qdrant_service import QdrantService

logger = logging.getLogger(__name__)


def parse_json_to_natural_language(data: dict) -> str:
    """
    NL Parsing: Chuyển đổi JSON thô thành văn bản tự nhiên.
    Giúp embedding capture ngữ nghĩa tốt hơn.
    """
    parts = []
    for key, value in data.items():
        if isinstance(value, dict):
            sub_parts = [f"{k}: {v}" for k, v in value.items()]
            parts.append(f"{key} gồm {', '.join(sub_parts)}")
        elif isinstance(value, list):
            parts.append(f"{key}: {', '.join(str(v) for v in value)}")
        else:
            parts.append(f"{key} là {value}")
    return ". ".join(parts)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Metadata Chunking: Chia nhỏ văn bản dài thành các đoạn nhỏ.
    Giữ overlap để không mất ngữ cảnh giữa các chunk.
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Cắt tại điểm ngắt câu gần nhất
        if end < len(text):
            last_period = chunk.rfind(".")
            last_newline = chunk.rfind("\n")
            cut_point = max(last_period, last_newline)
            if cut_point > chunk_size * 0.5:
                chunk = chunk[:cut_point + 1]
                end = start + cut_point + 1

        chunks.append(chunk.strip())
        start = end - overlap

    return [c for c in chunks if c]


def ingest_directory(
    directory: str,
    qdrant: QdrantService,
    embed_fn,
    category: Optional[str] = None,
) -> int:
    """
    Đọc tất cả file trong thư mục và đưa vào Qdrant.

    Args:
        directory: Đường dẫn thư mục chứa raw data.
        qdrant: Qdrant service instance.
        embed_fn: Hàm embedding (text -> vector).
        category: Category mặc định cho tất cả documents.

    Returns:
        Số lượng documents đã ingest.
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        logger.warning(f"Directory not found: {directory}")
        return 0

    total = 0

    for file_path in dir_path.rglob("*"):
        if file_path.is_dir():
            continue

        try:
            documents = _parse_file(file_path, category)
            if not documents:
                continue

            # Embed tất cả documents
            texts = [doc["text"] for doc in documents]
            vectors = [embed_fn(text) for text in texts]

            # Upsert vào Qdrant
            qdrant.upsert_documents(documents, vectors)
            total += len(documents)
            logger.info(f"Ingested {len(documents)} chunks from {file_path.name}")

        except Exception as e:
            logger.error(f"Error ingesting {file_path}: {e}")

    return total


def _parse_file(file_path: Path, category: Optional[str]) -> list[dict]:
    """Parse file thành danh sách documents."""
    suffix = file_path.suffix.lower()
    cat = category or file_path.parent.name or "general"

    if suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return [
                {
                    "text": parse_json_to_natural_language(item) if isinstance(item, dict) else str(item),
                    "metadata": {"category": cat, "source": file_path.name, "doc_id": f"{file_path.stem}-{i}"},
                }
                for i, item in enumerate(data)
            ]
        elif isinstance(data, dict):
            text = parse_json_to_natural_language(data)
            return [{"text": text, "metadata": {"category": cat, "source": file_path.name, "doc_id": file_path.stem}}]

    elif suffix in (".md", ".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = chunk_text(content)
        return [
            {
                "text": chunk,
                "metadata": {"category": cat, "source": file_path.name, "doc_id": f"{file_path.stem}-{i}"},
            }
            for i, chunk in enumerate(chunks)
        ]

    return []
