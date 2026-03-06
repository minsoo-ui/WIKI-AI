"""
Authentication API Endpoints
=============================
Quản lý đăng nhập, đăng xuất và chuyển đổi tài khoản.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class LoginRequest(BaseModel):
    """Schema đăng nhập."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema thông tin người dùng."""
    id: str
    username: str
    avatar_url: Optional[str] = None


class TokenResponse(BaseModel):
    """Schema token trả về sau đăng nhập."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Đăng nhập và nhận JWT token."""
    # TODO: Phase 02 - Kết nối SQLite + hash password
    return TokenResponse(
        access_token="placeholder-token",
        user=UserResponse(
            id="user-001",
            username=request.username,
            avatar_url=None,
        ),
    )


@router.post("/logout")
async def logout():
    """Đăng xuất (hủy session phía client)."""
    return {"message": "Đăng xuất thành công."}


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Lấy thông tin người dùng hiện tại."""
    # TODO: Phase 02 - Xác thực JWT
    return UserResponse(
        id="user-001",
        username="admin",
        avatar_url=None,
    )
