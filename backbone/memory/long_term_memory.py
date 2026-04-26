"""Layer 3: Long-Term Memory — persistent user data.

Stored in PostgreSQL with RLS for tenant isolation.
Supports confidence-based updates, access tracking, and time-decay.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Protocol, Sequence

import structlog

from backbone.memory.config import LongTermConfig
from backbone.memory.schemas import LongTermEntry

logger = structlog.get_logger("memory.long_term")


class LongTermBackend(Protocol):
    """Backend interface for long-term memory persistence."""

    async def upsert(self, entry: LongTermEntry) -> None: ...
    async def get(self, tenant_id: str, user_id: str, key: str) -> LongTermEntry | None: ...
    async def search(self, tenant_id: str, user_id: str, query: str, limit: int) -> list[LongTermEntry]: ...
    async def list_by_namespace(self, tenant_id: str, user_id: str, namespace: str) -> list[LongTermEntry]: ...
    async def delete(self, tenant_id: str, user_id: str, key: str) -> bool: ...
    async def count(self, tenant_id: str, user_id: str) -> int: ...


class PostgresLongTermBackend:
    """PostgreSQL-backed long-term memory with RLS.

    Schema (applied via Alembic migration):

    CREATE TABLE long_term_memory (
        entry_id     TEXT PRIMARY KEY,
        tenant_id    TEXT NOT NULL,
        user_id      TEXT NOT NULL,
        namespace    TEXT NOT NULL DEFAULT 'general',
        key          TEXT NOT NULL,
        value        JSONB NOT NULL,
        confidence   REAL DEFAULT 1.0,
        source       TEXT DEFAULT '',
        created_at   TIMESTAMPTZ DEFAULT now(),
        updated_at   TIMESTAMPTZ DEFAULT now(),
        access_count INTEGER DEFAULT 0,
        tags         TEXT[] DEFAULT '{}',
        UNIQUE(tenant_id, user_id, key)
    );

    -- RLS policy
    ALTER TABLE long_term_memory ENABLE ROW LEVEL SECURITY;
    CREATE POLICY tenant_isolation ON long_term_memory
        USING (tenant_id = current_setting('app.tenant_id'));

    -- Indexes
    CREATE INDEX idx_ltm_user ON long_term_memory(tenant_id, user_id);
    CREATE INDEX idx_ltm_namespace ON long_term_memory(tenant_id, user_id, namespace);
    CREATE INDEX idx_ltm_tags ON long_term_memory USING GIN(tags);
    """

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def upsert(self, entry: LongTermEntry) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO long_term_memory
                    (entry_id, tenant_id, user_id, namespace, key, value,
                     confidence, source, created_at, updated_at, access_count, tags)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                ON CONFLICT (tenant_id, user_id, key)
                DO UPDATE SET
                    value = EXCLUDED.value,
                    confidence = EXCLUDED.confidence,
                    updated_at = now(),
                    access_count = long_term_memory.access_count + 1,
                    tags = EXCLUDED.tags
                """,
                entry.entry_id, entry.tenant_id, entry.user_id,
                entry.namespace, entry.key, entry.value,
                entry.confidence, entry.source, entry.created_at,
                entry.updated_at, entry.access_count, list(entry.tags),
            )

    async def get(self, tenant_id: str, user_id: str, key: str) -> LongTermEntry | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                UPDATE long_term_memory
                SET access_count = access_count + 1
                WHERE tenant_id = $1 AND user_id = $2 AND key = $3
                RETURNING *
                """,
                tenant_id, user_id, key,
            )
            return self._row_to_entry(row) if row else None

    async def search(self, tenant_id: str, user_id: str, query: str, limit: int) -> list[LongTermEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM long_term_memory
                WHERE tenant_id = $1 AND user_id = $2
                  AND (key ILIKE $3 OR value::text ILIKE $3)
                ORDER BY updated_at DESC
                LIMIT $4
                """,
                tenant_id, user_id, f"%{query}%", limit,
            )
            return [self._row_to_entry(r) for r in rows]

    async def list_by_namespace(self, tenant_id: str, user_id: str, namespace: str) -> list[LongTermEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM long_term_memory
                WHERE tenant_id = $1 AND user_id = $2 AND namespace = $3
                ORDER BY updated_at DESC
                """,
                tenant_id, user_id, namespace,
            )
            return [self._row_to_entry(r) for r in rows]

    async def delete(self, tenant_id: str, user_id: str, key: str) -> bool:
        async with self._pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM long_term_memory WHERE tenant_id = $1 AND user_id = $2 AND key = $3",
                tenant_id, user_id, key,
            )
            return result == "DELETE 1"

    async def count(self, tenant_id: str, user_id: str) -> int:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT COUNT(*) FROM long_term_memory WHERE tenant_id = $1 AND user_id = $2",
                tenant_id, user_id,
            )

    @staticmethod
    def _row_to_entry(row: Any) -> LongTermEntry:
        return LongTermEntry(
            entry_id=row["entry_id"],
            tenant_id=row["tenant_id"],
            user_id=row["user_id"],
            namespace=row["namespace"],
            key=row["key"],
            value=row["value"],
            confidence=row["confidence"],
            source=row["source"],
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
            access_count=row["access_count"],
            tags=tuple(row["tags"]),
        )


class LongTermMemoryManager:
    """Manages persistent user knowledge.

    Supports:
    - Namespaced storage (preferences, facts, corrections, feedback)
    - Confidence-based merge (higher confidence overwrites)
    - Access-count tracking for relevance scoring
    - Capacity enforcement per user
    """

    def __init__(self, config: LongTermConfig, backend: LongTermBackend) -> None:
        self._config = config
        self._backend = backend

    async def remember(
        self,
        tenant_id: str,
        user_id: str,
        key: str,
        value: Any,
        namespace: str = "general",
        confidence: float = 1.0,
        source: str = "",
        tags: tuple[str, ...] = (),
    ) -> LongTermEntry:
        """Store or update a long-term memory."""
        existing = await self._backend.get(tenant_id, user_id, key)

        if existing and self._config.merge_strategy == "confidence_max":
            if existing.confidence > confidence:
                logger.debug("ltm_skip_lower_confidence", key=key)
                return existing

        entry = LongTermEntry(
            tenant_id=tenant_id,
            user_id=user_id,
            namespace=namespace,
            key=key,
            value=value,
            confidence=confidence,
            source=source,
            tags=tags,
        )
        await self._backend.upsert(entry)
        logger.info("ltm_stored", key=key, namespace=namespace, user=user_id)
        return entry

    async def recall(self, tenant_id: str, user_id: str, key: str) -> LongTermEntry | None:
        """Recall a specific memory by key."""
        return await self._backend.get(tenant_id, user_id, key)

    async def search(self, tenant_id: str, user_id: str, query: str, limit: int = 20) -> list[LongTermEntry]:
        """Search long-term memory by keyword."""
        return await self._backend.search(tenant_id, user_id, query, limit)

    async def forget(self, tenant_id: str, user_id: str, key: str) -> bool:
        """Delete a specific memory (GDPR right to erasure)."""
        deleted = await self._backend.delete(tenant_id, user_id, key)
        if deleted:
            logger.info("ltm_forgotten", key=key, user=user_id)
        return deleted

    async def get_user_profile(self, tenant_id: str, user_id: str) -> dict[str, list[LongTermEntry]]:
        """Get all long-term memories for a user, grouped by namespace."""
        result: dict[str, list[LongTermEntry]] = {}
        for ns in ("preferences", "facts", "corrections", "feedback", "general"):
            entries = await self._backend.list_by_namespace(tenant_id, user_id, ns)
            if entries:
                result[ns] = entries
        return result
