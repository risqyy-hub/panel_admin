"""
Konfigurasi aplikasi.
Semua rahasia dibaca dari file .env (environment variable), TIDAK di-hardcode.
"""

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

# Path .env berada di root folder backend/ (satu tingkat di atas folder app/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Setting aplikasi yang dibaca dari .env"""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database (MariaDB/MySQL via PyMySQL)
    DATABASE_URL: str = "mysql+pymysql://root:@127.0.0.1:3306/admin_dokter"

    # JWT
    JWT_SECRET: str = "ganti_dengan_secret_random"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS - frontend yang diizinkan
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Upload file
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5 MB
    UPLOAD_DIR: str = str(BASE_DIR / "uploads")


@lru_cache
def get_settings() -> Settings:
    """Singleton settings agar tidak dibaca ulang berulang kali."""
    return Settings()


settings = get_settings()
