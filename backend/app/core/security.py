"""
Security: bcrypt hashing, JWT, dan authorization (get_current_user / require_admin).
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import bcrypt
import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db

# Scheme Bearer token. auto_error=False supaya kita bisa mengirim format
# error 401 yang konsisten sendiri.
bearer_scheme = HTTPBearer(auto_error=False)


# ======================================================================
# PASSWORD HASHING (bcrypt - password plaintext TIDAK PERNAH disimpan)
# ======================================================================
def hash_password(password: str) -> str:
    """Meng-hash password dengan bcrypt (salt otomatis)."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Membandingkan password plaintext dengan hash tersimpan."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False


# ======================================================================
# JWT
# ======================================================================
def create_access_token(user_id: int, role: str) -> str:
    """Membuat JWT token dengan klaim sub (user id) dan role."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode & validasi JWT. Mengembalikan None bila token tidak valid/kadaluarsa."""
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None


# ======================================================================
# AUTHENTICATION & AUTHORIZATION DEPENDENCIES
# ======================================================================
def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    """
    Dependency: memvalidasi Bearer token dan mengembalikan objek User.
    Melempar 401 bila token tidak ada/tidak valid.
    """
    from app.models.user import User

    if credentials is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Token tidak ditemukan, silakan login terlebih dahulu")

    claims = decode_access_token(credentials.credentials)
    if claims is None or "sub" not in claims:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Token tidak valid atau sudah kedaluwarsa")

    user = db.get(User, int(claims["sub"]))
    if user is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Akun tidak ditemukan")

    if user.status != "active":
        from fastapi import HTTPException

        raise HTTPException(status_code=403, detail="Akun Anda tidak aktif")

    return user


def require_admin(current_user=Depends(get_current_user)):
    """
    Dependency: hanya akun dengan role 'admin' yang boleh mengakses
    endpoint admin. Semua endpoint admin WAJIB memakai ini.
    """
    from fastapi import HTTPException

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Akses ditolak: hanya admin yang diizinkan")
    return current_user
