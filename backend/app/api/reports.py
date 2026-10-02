"""Endpoint laporan user terhadap dokter (khusus admin)."""

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_admin
from app.schemas.report import ReportStatusUpdateRequest
from app.services import report_service
from app.utils import PaginationParams, ok, ok_list

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("")
def list_reports(
    search: Optional[str] = Query(None, description="Cari deskripsi/nama pelapor/dokter"),
    status: Optional[str] = Query(
        None, description="Filter: pending | reviewing | resolved | rejected"
    ),
    pagination: PaginationParams = Depends(),
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """List laporan. Contoh: GET /api/reports?page=1&limit=10&status=pending"""
    items, total = report_service.list_reports(
        db, pagination, search=search, status=status
    )
    return ok_list(items, page=pagination.page, limit=pagination.limit, total=total)


@router.get("/categories")
def list_categories(
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Daftar kategori laporan."""
    data = report_service.list_categories(db)
    return ok_list(data, page=1, limit=len(data) or 1, total=len(data), message="Berhasil")


@router.get("/{report_id}")
def get_report(
    report_id: int,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Detail laporan."""
    return ok("Berhasil", report_service.get_report(db, report_id))


@router.put("/{report_id}/status")
def update_report_status(
    report_id: int,
    payload: ReportStatusUpdateRequest,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Mengubah status laporan + catatan admin.
    CATATAN: dokter TIDAK otomatis dihukum - hanya status laporan yang berubah.
    """
    data = report_service.update_report_status(db, admin.id, report_id, payload)
    return ok("Status laporan berhasil diperbarui", data)
