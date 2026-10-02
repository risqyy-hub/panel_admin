"""Helper response, pagination, dan utilitas umum backend."""

from typing import Any, Dict, List, Optional

from fastapi import Query
from sqlalchemy.orm import Session


def ok(message: str = "Berhasil", data: Any = None) -> Dict[str, Any]:
    """Response sukses standar: {"success": true, "message": "...", "data": {...}}"""
    return {"success": True, "message": message, "data": data}


def ok_list(
    items: List[Any],
    page: int,
    limit: int,
    total: int,
    message: str = "Berhasil",
) -> Dict[str, Any]:
    """
    Response sukses untuk list dengan pagination:
    {
      "success": true, "message": "...",
      "data": [...],
      "pagination": {"page": 1, "limit": 10, "total": 100, "total_pages": 10}
    }
    """
    total_pages = max(1, -(-total // limit)) if limit > 0 else 1
    return {
        "success": True,
        "message": message,
        "data": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
        },
    }


def fail(message: str) -> Dict[str, str]:
    """Response gagal standar: {"success": false, "message": "..."}"""
    return {"success": False, "message": message}


class PaginationParams:
    """Parameter pagination bawaan FastAPI: ?page=1&limit=10"""

    def __init__(
        self,
        page: int = Query(1, ge=1, description="Nomor halaman"),
        limit: int = Query(10, ge=1, le=100, description="Jumlah data per halaman"),
    ):
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit


def paginate_query(query, pagination: PaginationParams, session: Session):
    """Menjalankan query dengan offset/limit dan menghitung total baris."""
    total = query.count()
    items = query.offset(pagination.offset).limit(pagination.limit).all()
    return items, total
