"""
Application Configuration
Quản lý toàn bộ cấu hình từ biến môi trường (.env)
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Cấu hình chính của ứng dụng WIKI-AI."""

    # --- App ---
    APP_NAME: str = "WIKI-AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- Database ---
    SQLITE_URL: str = "sqlite+aiosqlite:///./data/wiki_ai.db"

    # --- Qdrant Vector DB ---
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "wiki_documents"
    QDRANT_USE_LOCAL: bool = True
    QDRANT_LOCAL_PATH: str = "./data/qdrant_storage"

    # --- Embedding Model ---
    EMBEDDING_MODEL: str = "nomic-ai/nomic-embed-text-v1.5"
    EMBEDDING_DIMENSION: int = 768

    # --- LLM ---
    LLM_MODEL: str = "Qwen/Qwen2.5-1.5B-Instruct"
    LLM_BACKEND: str = "ipex-llm"  # ipex-llm | ollama | llamacpp

    # --- Redis (Memory) ---
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_ENABLED: bool = False

    # --- LangFuse (Observability) ---
    LANGFUSE_ENABLED: bool = False
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "http://localhost:3000"

    # --- Auth ---
    SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Singleton pattern cho Settings."""
    return Settings()
