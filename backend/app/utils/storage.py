"""Helper penyimpanan file upload (aman: validasi MIME, ukuran, nama file)."""

import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import UploadFile

from app.core.config import settings

# MIME type yang diizinkan untuk gambar
ALLOWED_IMAGE_MIME = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}

# MIME type yang diizinkan untuk dokumen
ALLOWED_DOC_MIME = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
}


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _safe_name() -> str:
    """Nama file acak yang aman (tanpa karakter berbahaya)."""
    return uuid.uuid4().hex


async def save_image_upload(file: UploadFile, subfolder: str = "sliders") -> Optional[str]:
    """
    Menyimpan upload gambar dengan aman.
    Mengembalikan path relatif (mis. /uploads/sliders/abc123.jpg)
    atau None bila file tidak dikirim.
    """
    if file is None or file.filename in (None, ""):
        return None

    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_IMAGE_MIME:
        raise ValueError(
            "Format file tidak didukung. Gunakan JPG, PNG, WEBP, atau GIF."
        )

    # Batas ukuran 5 MB
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise ValueError("Ukuran gambar maksimal 5 MB.")

    ext = ALLOWED_IMAGE_MIME[content_type]
    folder = Path(settings.UPLOAD_DIR) / subfolder
    _ensure_dir(folder)

    filename = f"{_safe_name()}{ext}"
    (folder / filename).write_bytes(content)
    return f"/uploads/{subfolder}/{filename}"


def delete_uploaded_file(relative_path: Optional[str]) -> None:
    """Menghapus file upload berdasarkan path relatif /uploads/... (best effort)."""
    if not relative_path or not relative_path.startswith("/uploads/"):
        return
    try:
        # Normalisasi path & pastikan tetap di dalam folder uploads (anti path traversal)
        base = Path(settings.UPLOAD_DIR).resolve()
        target = (base / relative_path.replace("/uploads/", "", 1)).resolve()
        if str(target).startswith(str(base)) and os.path.isfile(target):
            os.remove(target)
    except OSError:
        pass
