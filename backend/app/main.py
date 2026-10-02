"""
Entry point backend FastAPI - ADMIN DOKTER.

Jalankan dari folder backend/:
    ..venv\\Scripts\\Activate.ps1
    fastapi dev app/main.py
"""

from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import auth, dashboard, doctors, reports, sliders, users
from app.core.config import settings
from app.utils import fail

app = FastAPI(
    title="ADMIN DOKTER API",
    description="REST API admin panel aplikasi dokter (FastAPI + MariaDB).",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ======================================================================
# CORS - hanya origin frontend yang diizinkan.
# JANGAN pakai ["*"] di production.
# ======================================================================
cors_origins: List[str] = list(settings.BACKEND_CORS_ORIGINS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================================
# FORMAT RESPONSE ERROR YANG KONSISTEN
# {"success": false, "message": "..."}
# ======================================================================
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail
    if isinstance(detail, dict):
        return JSONResponse(status_code=exc.status_code, content=detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=fail(str(detail)),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = []
    for err in exc.errors():
        loc = ".".join(str(x) for x in err.get("loc", []) if x != "body")
        msg = err.get("msg", "Data tidak valid")
        messages.append(f"{loc}: {msg}" if loc else msg)
    return JSONResponse(
        status_code=422,
        content=fail("; ".join(messages) or "Data tidak valid"),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Jangan bocorkan detail internal ke klien
    return JSONResponse(
        status_code=500,
        content=fail("Terjadi kesalahan pada server. Silakan coba lagi."),
    )


# ======================================================================
# STATIC FILES - upload gambar slider & dokumen
# ======================================================================
upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")


# ======================================================================
# ROUTES
# ======================================================================
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(doctors.router)
app.include_router(users.router)
app.include_router(sliders.router)
app.include_router(reports.router)


@app.get("/", tags=["Health"])
def root():
    """Health check API."""
    return {
        "success": True,
        "message": "ADMIN DOKTER API berjalan",
        "docs": "/docs",
    }


@app.get("/api/health", tags=["Health"])
def health():
    """Health check terpisah untuk monitoring frontend."""
    return {"success": True, "message": "OK"}
