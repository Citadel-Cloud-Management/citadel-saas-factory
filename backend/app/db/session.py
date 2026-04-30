"""Async SQLAlchemy engine and session factory."""

import os
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://citadel:citadel@localhost:5432/citadel",
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def set_tenant_context(session: AsyncSession, tenant_id: str) -> None:
    """Set the current tenant for row-level security enforcement.

    Executes SET LOCAL so the setting is scoped to the current transaction.
    RLS policies in PostgreSQL should reference current_setting('app.current_tenant').
    """
    await session.execute(
        text("SET LOCAL app.current_tenant = :tenant_id"),
        {"tenant_id": tenant_id},
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency-injectable async session generator.

    Usage in FastAPI:
        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_factory() as session:
        async with session.begin():
            yield session
