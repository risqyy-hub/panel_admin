"""Model tabel users."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # bcrypt hash
    phone: Mapped[Optional[str]] = mapped_column(String(30), default=None)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")  # admin|doctor|user
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")  # active|inactive|suspended
    avatar: Mapped[Optional[str]] = mapped_column(String(255), default=None)
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
    doctor: Mapped[Optional["Doctor"]] = relationship(  # type: ignore[name-defined]
        "Doctor", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    reports: Mapped[List["Report"]] = relationship(  # type: ignore[name-defined]
        "Report", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role})>"
