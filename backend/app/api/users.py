"""Endpoint manajemen user (khusus admin)."""

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_admin
from app.services import user_service
from app.utils import PaginationParams, ok, ok_list

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("")
def list_users(
    search: Optional[str] = Query(None, description="Cari nama/email/telepon"),
    status: Optional[str] = Query(
        None, description="Filter status: active | inactive | suspended"
    ),
    role: Optional[str] = Query(None, description="Filter role: admin | doctor | user"),
    pagination: PaginationParams = Depends(),
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """List user. Contoh: GET /api/users?page=1&limit=10&search=budi&status=active"""
    items, total = user_service.list_users(
        db, pagination, search=search, status=status, role=role
    )
    return ok_list(items, page=pagination.page, limit=pagination.limit, total=total)


@router.get("/{user_id}")
def get_user(
    user_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Detail user (termasuk info dokter bila role=doctor)."""
    return ok("Berhasil", user_service.get_user(db, user_id))


@router.put("/{user_id}/activate")
def activate_user(
    user_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Mengaktifkan user."""
    data = user_service.set_user_status(db, user_id, admin.id, status="active")
    return ok("Akun user diaktifkan", data)


@router.put("/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Menonaktifkan user."""
    data = user_service.set_user_status(db, user_id, admin.id, status="inactive")
    return ok("Akun user dinonaktifkan", data)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Menghapus user (operasi berbahaya - konfirmasi wajib di frontend)."""
    user_service.delete_user(db, user_id, admin.id)
    return ok("User berhasil dihapus")
