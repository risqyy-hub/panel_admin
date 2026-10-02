"""Schema autentikasi: login, token, dan profil."""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Body request POST /api/auth/login"""

    email: EmailStr = Field(..., description="Email admin")
    password: str = Field(..., min_length=1, description="Password")
    remember_me: bool = Field(default=False, description="Ingat sesi login")


class TokenResponse(BaseModel):
    """Response sukses login."""

    access_token: str
    token_type: str = "bearer"
    user: "UserBrief"


class UserBrief(BaseModel):
    """Ringkasan profil user untuk response auth."""

    id: int
    name: str
    email: str
    role: str
    status: str
    avatar: Optional[str] = None
    phone: Optional[str] = None

    model_config = {"from_attributes": True}


class MeResponse(UserBrief):
    """Response GET /api/auth/me (identik dengan UserBrief)."""
