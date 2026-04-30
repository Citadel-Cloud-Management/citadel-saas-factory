"""Tenant service — business logic for tenant management."""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tenant import Tenant
from app.repositories.tenant import TenantRepository
from app.schemas.tenant import TenantCreate, TenantUpdate


class TenantService:
    """Orchestrates tenant-related business logic."""

    def __init__(self, session: AsyncSession) -> None:
        self._repo = TenantRepository(session)

    async def create_tenant(self, data: TenantCreate) -> Tenant:
        """Create a new tenant. Raises ValueError if slug is taken."""
        existing = await self._repo.get_by_slug(data.slug)
        if existing is not None:
            msg = f"Tenant with slug {data.slug!r} already exists"
            raise ValueError(msg)

        return await self._repo.create(
            name=data.name,
            slug=data.slug,
            plan=data.plan,
        )

    async def get_tenant(self, tenant_id: uuid.UUID) -> Tenant | None:
        """Fetch a tenant by ID."""
        return await self._repo.get_by_id(tenant_id)

    async def get_tenant_by_slug(self, slug: str) -> Tenant | None:
        """Fetch a tenant by slug."""
        return await self._repo.get_by_slug(slug)

    async def update_tenant(
        self,
        tenant_id: uuid.UUID,
        data: TenantUpdate,
    ) -> Tenant | None:
        """Update tenant fields. Returns None if not found."""
        update_fields = data.model_dump(exclude_unset=True)
        if not update_fields:
            return await self._repo.get_by_id(tenant_id)
        return await self._repo.update(tenant_id, **update_fields)

    async def list_tenants(
        self,
        *,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[Tenant], int]:
        """List tenants with pagination."""
        return await self._repo.get_all(page=page, limit=limit)
