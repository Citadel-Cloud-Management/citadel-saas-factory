"""Generic async repository — CRUD operations with tenant isolation."""

import uuid
from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Generic async repository providing CRUD with optional tenant filtering.

    Subclass and set `model` to the SQLAlchemy model class.
    If the model has a `tenant_id` column, queries are automatically
    filtered by the provided tenant_id.
    """

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def _is_tenant_scoped(self) -> bool:
        return hasattr(self.model, "tenant_id")

    def _apply_tenant_filter(
        self,
        stmt: Any,
        tenant_id: uuid.UUID | None,
    ) -> Any:
        if self._is_tenant_scoped and tenant_id is not None:
            stmt = stmt.where(self.model.tenant_id == tenant_id)  # type: ignore[attr-defined]
        return stmt

    async def get_by_id(
        self,
        entity_id: uuid.UUID,
        tenant_id: uuid.UUID | None = None,
    ) -> ModelT | None:
        """Fetch a single record by primary key."""
        stmt = select(self.model).where(self.model.id == entity_id)
        stmt = self._apply_tenant_filter(stmt, tenant_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        tenant_id: uuid.UUID | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[ModelT], int]:
        """Fetch a paginated list of records and total count."""
        base = select(self.model)
        base = self._apply_tenant_filter(base, tenant_id)

        count_stmt = select(func.count()).select_from(base.subquery())
        total_result = await self._session.execute(count_stmt)
        total = total_result.scalar_one()

        offset = (page - 1) * limit
        data_stmt = base.offset(offset).limit(limit)
        data_result = await self._session.execute(data_stmt)
        items = list(data_result.scalars().all())

        return items, total

    async def create(self, **kwargs: Any) -> ModelT:
        """Insert a new record and return it."""
        instance = self.model(**kwargs)
        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def update(
        self,
        entity_id: uuid.UUID,
        tenant_id: uuid.UUID | None = None,
        **kwargs: Any,
    ) -> ModelT | None:
        """Update an existing record. Returns None if not found."""
        instance = await self.get_by_id(entity_id, tenant_id)
        if instance is None:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(instance, key, value)
        await self._session.flush()
        await self._session.refresh(instance)
        return instance

    async def delete(
        self,
        entity_id: uuid.UUID,
        tenant_id: uuid.UUID | None = None,
    ) -> bool:
        """Delete a record by ID. Returns True if deleted."""
        instance = await self.get_by_id(entity_id, tenant_id)
        if instance is None:
            return False
        await self._session.delete(instance)
        await self._session.flush()
        return True
