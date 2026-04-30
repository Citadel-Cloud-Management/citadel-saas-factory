"""Dependency injection helpers for API routes."""

from collections.abc import AsyncGenerator
from typing import Any

from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db, set_tenant_context


async def get_current_user(request: Request) -> dict[str, Any]:
    """Extract authenticated user from request state.

    The AuthMiddleware decodes the JWT and stores the payload
    in ``request.state.user``.  This dependency simply surfaces
    that data (or rejects unauthenticated requests).
    """
    user: dict[str, Any] | None = getattr(request.state, "user", None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_tenant(request: Request) -> str:
    """Extract tenant ID set by TenantMiddleware."""
    tenant_id: str | None = getattr(request.state, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context required",
        )
    return tenant_id


def require_superuser(user: dict[str, Any]) -> dict[str, Any]:
    """Raise 403 if the user does not have superuser privileges.

    Checks for ``is_superuser`` claim or ``superuser`` / ``admin``
    in the ``roles`` list of the decoded JWT payload.
    """
    is_super = user.get("is_superuser", False)
    roles: list[str] = user.get("roles", [])
    if not is_super and "superuser" not in roles and "admin" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser privileges required",
        )
    return user


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Yield an async DB session with tenant context applied.

    Wraps :func:`get_db` and calls :func:`set_tenant_context` so
    that PostgreSQL row-level security policies are enforced.
    """
    tenant_id: str | None = getattr(request.state, "tenant_id", None)
    async for session in get_db():
        if tenant_id:
            await set_tenant_context(session, tenant_id)
        yield session
