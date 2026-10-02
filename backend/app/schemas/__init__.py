"""Package schemas (Pydantic) untuk validasi input/output API."""

from app.schemas.auth import LoginRequest, TokenResponse, MeResponse
from app.schemas.user import UserOut
from app.schemas.doctor import DoctorOut, DoctorRejectRequest
from app.schemas.slider import SliderOut
from app.schemas.report import ReportOut, ReportStatusUpdateRequest

__all__ = [
    "LoginRequest",
    "TokenResponse",
    "MeResponse",
    "UserOut",
    "DoctorOut",
    "DoctorRejectRequest",
    "SliderOut",
    "ReportOut",
    "ReportStatusUpdateRequest",
]
