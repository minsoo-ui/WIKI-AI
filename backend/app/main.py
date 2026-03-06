"""
WIKI-AI Backend - FastAPI Entry Point
=====================================
Local Multi-Agent System optimized for Intel i3-12100 & UHD 730 (SYCL).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api import router as api_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Local AI Agent for WIKI-Database with Advanced RAG & Multi-agent Architecture.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- CORS (cho phép Frontend gọi API) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Health Check ---
@app.get("/health", tags=["System"])
async def health_check():
    """Kiểm tra server có đang hoạt động hay không."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/system/status", tags=["System"])
async def system_status():
    """Kiểm tra trạng thái chi tiết của các services (LLM, Embedding, Qdrant)."""
    from app.dependencies import get_system_status
    return get_system_status()



# --- Mount API Router ---
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
