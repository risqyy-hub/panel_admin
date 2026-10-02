"""Schema dokter."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DoctorDocumentOut(BaseModel):
    """Item dokumen pendukung dokter."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    document_type: str
    document_path: str
    verification_status: str
    created_at: Optional[datetime] = None


class DoctorOut(BaseModel):
    """Response dokter (list & detail), field user digabung ke level atas."""

    id: int
    user_id: int
    name: str
    email: str
    phone: Optional[str] = None
    avatar: Optional[str] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    bio: Optional[str] = None
    verification_status: str
    rejection_reason: Optional[str] = None
    verified_at: Optional[datetime] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    documents: List[DoctorDocumentOut] = Field(default_factory=list)


class DoctorRejectRequest(BaseModel):
    """Body request PUT /api/doctors/{id}/reject - alasan WAJIB diisi."""

    reason: str = Field(..., min_length=5, description="Alasan penolakan")
