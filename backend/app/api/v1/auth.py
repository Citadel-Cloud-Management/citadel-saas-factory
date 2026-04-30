"""Authentication endpoints — login, register, me, refresh."""

import os
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db_session
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24
REFRESH_TOKEN_EXPIRE_HOURS = 168  # 7 days


def _create_access_token(user_id: str, email: str, tenant_id: str) -> str:
    """Create a signed JWT access token with standard claims."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "tenant_id": tenant_id,
        "iat": now,
        "exp": now + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
        "type": "access",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def _create_refresh_token(user_id: str) -> str:
    """Create a signed JWT refresh token."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS),
        "type": "refresh",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def _envelope(data: Any, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """Wrap a response in the standard envelope."""
    return {"data": data, "error": None, "meta": meta or {}}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Authenticate a user and return a JWT token pair.

    Accepts ``email`` and ``password`` in the JSON body.
    """
    body = await request.json()
    email: str | None = body.get("email")
    password: str | None = body.get("password")
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="email and password are required",
        )

    service = UserService(db)
    user = await service.authenticate(email=email, password=password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = _create_access_token(
        user_id=str(user.id),
        email=user.email,
        tenant_id=str(user.tenant_id),
    )
    refresh_token = _create_refresh_token(user_id=str(user.id))

    return _envelope({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    })


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Register a new user account."""
    body = await request.json()
    service = UserService(db)
    try:
        user = await service.create_user(data=body)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
    return _envelope({
        "id": str(user.id),
        "email": user.email,
        "tenant_id": str(user.tenant_id),
    })


@router.get("/me", status_code=status.HTTP_200_OK)
async def me(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Return the currently authenticated user's profile."""
    return _envelope({
        "user_id": current_user.get("sub"),
        "email": current_user.get("email"),
        "tenant_id": current_user.get("tenant_id"),
        "roles": current_user.get("roles", []),
    })


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(request: Request) -> dict[str, Any]:
    """Exchange a valid refresh token for a new access token."""
    body = await request.json()
    refresh_token: str | None = body.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="refresh_token is required",
        )

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is not a refresh token",
        )

    user_id = payload["sub"]
    # Note: email/tenant_id would be looked up from DB in production;
    # for now we reuse claims from the refresh payload if available.
    access_token = _create_access_token(
        user_id=user_id,
        email=payload.get("email", ""),
        tenant_id=payload.get("tenant_id", ""),
    )
    new_refresh = _create_refresh_token(user_id=user_id)

    return _envelope({
        "access_token": access_token,
        "refresh_token": new_refresh,
        "token_type": "bearer",
    })
