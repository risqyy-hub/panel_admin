"""Model tabel doctors."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    specialization: Mapped[Optional[str]] = mapped_column(String(120), default=None)
    license_number: Mapped[Optional[str]] = mapped_column(String(80), default=None)  # STR/SIP
    education: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    experience: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    bio: Mapped[Optional[str]] = mapped_column(Text, default=None)
    verification_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending", index=True
    )  # pending|approved|rejected
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, default=None)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    # Relasi
    user: Mapped["User"] = relationship("User", back_populates="doctor")  # type: ignore[name-defined]
    documents: Mapped[List["DoctorDocument"]] = relationship(  # type: ignore[name-defined]
        "DoctorDocument", back_populates="doctor", cascade="all, delete-orphan"
    )
    reports: Mapped[List["Report"]] = relationship(  # type: ignore[name-defined]
        "Report", back_populates="doctor", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Doctor {self.id} {self.specialization}>"
