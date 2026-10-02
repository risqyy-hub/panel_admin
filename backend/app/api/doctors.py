"""Endpoint manajemen & verifikasi dokter (khusus admin)."""

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_admin
from app.schemas.doctor import DoctorRejectRequest
from app.services import doctor_service
from app.utils import PaginationParams, ok, ok_list

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])


@router.get("")
def list_doctors(
    search: Optional[str] = Query(None, description="Cari nama/email/spesialisasi/STR"),
    status: Optional[str] = Query(
        None, description="Filter status: pending | approved | rejected"
    ),
    pagination: PaginationParams = Depends(),
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    List dokter.
    Contoh: GET /api/doctors?page=1&limit=10&search=andi&status=pending
    """
    items, total = doctor_service.list_doctors(db, pagination, search=search, status=status)
    return ok_list(items, page=pagination.page, limit=pagination.limit, total=total)


@router.get("/{doctor_id}")
def get_doctor(
    doctor_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Detail dokter + dokumen pendukung."""
    return ok("Berhasil", doctor_service.get_doctor(db, doctor_id))


@router.put("/{doctor_id}/approve")
def approve_doctor(
    doctor_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Menyetujui verifikasi dokter."""
    data = doctor_service.approve_doctor(db, doctor_id, admin.id)
    return ok("Dokter berhasil diverifikasi", data)


@router.put("/{doctor_id}/reject")
def reject_doctor(
    doctor_id: int,
    payload: DoctorRejectRequest,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Menolak verifikasi dokter (alasan wajib diisi)."""
    data = doctor_service.reject_doctor(db, doctor_id, admin.id, payload)
    return ok("Verifikasi dokter ditolak", data)


@router.put("/{doctor_id}/activate")
def activate_doctor(
    doctor_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Mengaktifkan akun dokter."""
    data = doctor_service.set_doctor_active(db, doctor_id, admin.id, active=True)
    return ok("Akun dokter diaktifkan", data)


@router.put("/{doctor_id}/deactivate")
def deactivate_doctor(
    doctor_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Menonaktifkan akun dokter."""
    data = doctor_service.set_doctor_active(db, doctor_id, admin.id, active=False)
    return ok("Akun dokter dinonaktifkan", data)
