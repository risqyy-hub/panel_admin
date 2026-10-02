"""
Koneksi database (SQLAlchemy 2.x) ke MariaDB/MySQL.

- Engine dibuat dari DATABASE_URL di .env
- SessionLocal dipakai oleh dependency get_db()
- Base adalah deklaratif base untuk seluruh model ORM
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # cek koneksi sebelum dipakai (menghindari "MySQL server has gone away")
    pool_recycle=3600,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class untuk seluruh model ORM."""


def get_db() -> Generator[Session, None, None]:
    """Dependency FastAPI: menyediakan session database per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
