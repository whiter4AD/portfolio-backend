from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.config import settings
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    require_auth,
)

router = APIRouter()


# ── Response schema ───────────────────────────────────────────────
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


# ── POST /api/auth/login ──────────────────────────────────────────
@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends()):
    """
    Exchange username + password for a JWT access token.
    Use the token as:  Authorization: Bearer <token>
    """
    if form.username != settings.ADMIN_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not verify_password(form.password, settings.ADMIN_PASSWORD_HASH):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token({"sub": form.username})
    return TokenOut(
        access_token=token,
        expires_in=settings.JWT_EXPIRE_MINUTES * 60,
    )


# ── GET /api/auth/me ──────────────────────────────────────────────
@router.get("/me")
def me(current_user: dict = Depends(require_auth)):
    """Check your current token — returns your username if valid."""
    return {"username": current_user["username"], "status": "authenticated"}


# ── GET /api/auth/hashpw?password=xxx ────────────────────────────
# Use this ONCE to generate your ADMIN_PASSWORD_HASH for .env
# Then remove or disable this endpoint in production!
@router.get("/hashpw", include_in_schema=False)
def hashpw(password: str):
    """
    Helper: generate a bcrypt hash for your password.
    Paste the result into ADMIN_PASSWORD_HASH in .env
    DELETE or protect this route after first use.
    """
    return {"hash": hash_password(password)}
