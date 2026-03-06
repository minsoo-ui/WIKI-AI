"""
API Router - Gom tất cả endpoints vào một router chính.
"""
from fastapi import APIRouter

from app.api.chat import router as chat_router
from app.api.auth import router as auth_router

router = APIRouter()

# --- Chat endpoints ---
router.include_router(chat_router, prefix="/chat", tags=["Chat"])

# --- Auth endpoints ---
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
