"""Tenant management endpoints — CRUD operations on tenants."""

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.auth import Permission, require_permission
from app.services.tenant_service import TenantService

router = APIRouter(prefix="/tenants", tags=["tenants"])


def _envelope(
    data: Any,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Wrap a response in the standard envelope."""
    return {"data": data, "error": None, "meta": meta or {}}


def _tenant_dict(tenant: Any) -> dict[str, Any]:
    """Serialise a tenant model to a response dict."""
    return {
        "id": str(tenant.id),
        "name": tenant.name,
        "slug": getattr(tenant, "slug", None),
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def list_tenants(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict[str, Any] = Depends(require_permission(Permission.TENANTS_READ)),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """List all tenants (admin+ role required)."""

    service = TenantService(db)
    tenants, total = await service.list_tenants(page=page, limit=limit)
    return _envelope(
        data=[_tenant_dict(t) for t in tenants],
        meta={"total": total, "page": page, "limit": limit},
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tenant(
    request: Request,
    current_user: dict[str, Any] = Depends(require_permission(Permission.TENANTS_WRITE)),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Create a new tenant (admin+ role required)."""

    body = await request.json()
    service = TenantService(db)
    try:
        tenant = await service.create_tenant(data=body)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
    return _envelope(_tenant_dict(tenant))


@router.get("/{tenant_id}", status_code=status.HTTP_200_OK)
async def get_tenant(
    tenant_id: UUID,
    current_user: dict[str, Any] = Depends(require_permission(Permission.TENANTS_READ)),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Get a tenant by ID (admin+ role required)."""
    caller_tenant = current_user.get("tenant_id")
    is_own = caller_tenant == str(tenant_id)
    role: str = current_user.get("role", "member")
    is_privileged = role in {"admin", "owner", "superuser"}

    if not is_own and not is_privileged:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to own tenant",
        )

    service = TenantService(db)
    tenant = await service.get_tenant(tenant_id=str(tenant_id))
    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    return _envelope(_tenant_dict(tenant))


@router.put("/{tenant_id}", status_code=status.HTTP_200_OK)
async def update_tenant(
    tenant_id: UUID,
    request: Request,
    current_user: dict[str, Any] = Depends(require_permission(Permission.TENANTS_WRITE)),
    db: AsyncSession = Depends(get_db_session),
) -> dict[str, Any]:
    """Update a tenant (admin+ role required)."""

    body = await request.json()
    service = TenantService(db)
    updated = await service.update_tenant(tenant_id=str(tenant_id), data=body)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    return _envelope(_tenant_dict(updated))
