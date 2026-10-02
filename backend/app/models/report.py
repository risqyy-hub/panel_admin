"""Model tabel reports dan report_categories."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReportCategory(Base):
    __tablename__ = "report_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    reports: Mapped[List["Report"]] = relationship("Report", back_populates="category")

    def __repr__(self) -> str:
        return f"<ReportCategory {self.name}>"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("report_categories.id", ondelete="SET NULL", onupdate="CASCADE"),
        default=None,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[Optional[str]] = mapped_column(String(255), default=None)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending", index=True)
    admin_note: Mapped[Optional[str]] = mapped_column(Text, default=None)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=None)
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
    user: Mapped["User"] = relationship("User", back_populates="reports")  # type: ignore[name-defined]
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="reports")  # type: ignore[name-defined]
    category: Mapped[Optional[ReportCategory]] = relationship(
        "ReportCategory", back_populates="reports"
    )

    def __repr__(self) -> str:
        return f"<Report {self.id} ({self.status})>"
