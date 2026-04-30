"""User repository — data access for User model."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User CRUD and tenant-scoped queries."""

    model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_email(self, email: str) -> User | None:
        """Find a user by email address (globally unique)."""
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_users(
        self,
        tenant_id: uuid.UUID,
        *,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[User], int]:
        """Fetch paginated active users within a tenant."""
        stmt = (
            select(User)
            .where(User.tenant_id == tenant_id, User.is_active.is_(True))
        )
        return await self._paginate(stmt, page=page, limit=limit)

    async def _paginate(
        self,
        stmt,
        *,
        page: int,
        limit: int,
    ) -> tuple[list[User], int]:
        """Run a paginated query, returning (items, total_count)."""
        from sqlalchemy import func

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self._session.execute(count_stmt)
        total = total_result.scalar_one()

        offset = (page - 1) * limit
        data_result = await self._session.execute(stmt.offset(offset).limit(limit))
        items = list(data_result.scalars().all())

        return items, total
