"""Endpoint autentikasi: /api/auth/login, /api/auth/me, /api/auth/logout."""

from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.auth import LoginRequest
from app.services import auth_service
from app.utils import ok

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Login admin/user.
    Response: {"success": true, "message": "...", "data": {"access_token": "...", "user": {...}}}
    """
    user = auth_service.authenticate(db, payload)
    token = auth_service.issue_token(db, user)
    return ok(
        "Login berhasil",
        {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "status": user.status,
                "avatar": user.avatar,
                "phone": user.phone,
            },
        },
    )


@router.get("/me")
def me(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Mengembalikan profil user dari token yang valid."""
    return ok(
        "Berhasil",
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "status": user.status,
            "avatar": user.avatar,
            "phone": user.phone,
        },
    )


@router.post("/logout")
def logout(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Mencatat logout. Token dihapus di sisi klien (localStorage/cookie)."""
    auth_service.logout(db, user)
    return ok("Logout berhasil")
