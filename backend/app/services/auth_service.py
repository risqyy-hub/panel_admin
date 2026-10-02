"""Service autentikasi: login, profil, logout."""

from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.utils.activity import log_admin_activity


def authenticate(db: Session, payload: LoginRequest) -> User:
    """
    Verifikasi email + password.
    Pesan error sengaja dibuat sama untuk email tidak ditemukan & password salah
    agar tidak membocorkan keberadaan akun (email enumeration).
    """
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()

    if user is None or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    if user.status != "active":
        raise HTTPException(status_code=403, detail="Akun Anda tidak aktif. Hubungi administrator.")

    return user


def issue_token(db: Session, user: User) -> str:
    """Membuat JWT untuk user dan mencatat aktivitas login."""
    token = create_access_token(user_id=user.id, role=user.role)
    log_admin_activity(
        db,
        admin_id=user.id,
        action="login",
        target_type="user",
        target_id=user.id,
        description=f"{user.email} login ke aplikasi",
    )
    db.commit()
    return token


def logout(db: Session, user: Optional[User]) -> None:
    """Mencatat aktivitas logout (token dibuang di sisi klien)."""
    if user is not None:
        log_admin_activity(
            db,
            admin_id=user.id,
            action="logout",
            target_type="user",
            target_id=user.id,
            description=f"{user.email} logout",
        )
        db.commit()
