"""User management endpoints — CRUD operations on users."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.auth import Permission, require_permission
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def _envelope(
    data: Any,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Wrap a response in the standard envelope."""
    return {"data": data, "error": None, "meta": meta or {}}


@router.get("/", status_code=status.HTTP_200_OK)
async def list_users(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict[str, Any] = Depends(require_permission(Permission.USERS_READ)),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """List users in the current tenant (paginated)."""
    tenant_id = current_user.get("tenant_id")
    service = UserService(db)
    users, total = await service.list_users(
        tenant_id=tenant_id,
        page=page,
        limit=limit,
    )
    return _envelope(
        data=[
            {"id": str(u.id), "email": u.email, "tenant_id": str(u.tenant_id)}
            for u in users
        ],
        meta={"total": total, "page": page, "limit": limit},
    )


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id: UUID,
    current_user: dict[str, Any] = Depends(require_permission(Permission.USERS_READ)),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Retrieve a single user by ID."""
    service = UserService(db)
    user = await service.get_user(user_id=str(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return _envelope({
        "id": str(user.id),
        "email": user.email,
        "tenant_id": str(user.tenant_id),
    })


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: UUID,
    request: Request,
    current_user: dict[str, Any] = Depends(require_permission(Permission.USERS_WRITE)),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Update a user.  Only the user themselves or a privileged role may update."""
    caller_id = current_user.get("sub")
    is_self = caller_id == str(user_id)
    role: str = current_user.get("role", "member")
    is_privileged = role in {"admin", "owner", "superuser"}

    if not is_self and not is_privileged:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile",
        )

    body = await request.json()
    service = UserService(db)
    updated = await service.update_user(user_id=str(user_id), data=body)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return _envelope({
        "id": str(updated.id),
        "email": updated.email,
        "tenant_id": str(updated.tenant_id),
    })


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: UUID,
    current_user: dict[str, Any] = Depends(require_permission(Permission.USERS_DELETE)),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Soft-delete a user (admin+ role required)."""

    service = UserService(db)
    deleted = await service.delete_user(user_id=str(user_id))
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return _envelope({"deleted": True, "user_id": str(user_id)})
