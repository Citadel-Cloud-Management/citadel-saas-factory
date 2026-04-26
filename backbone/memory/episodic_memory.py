"""Layer 4: Episodic Memory — timestamped interaction events.

Append-only event log stored in PostgreSQL (or TimescaleDB for time-series optimization).
Each episode is also optionally embedded for similarity search via the semantic layer.
"""

from __future__ import annotations

from typing import Any, Protocol

import structlog

from backbone.memory.config import EpisodicConfig
from backbone.memory.schemas import EpisodicEntry, EpisodeKind

logger = structlog.get_logger("memory.episodic")


class EpisodicBackend(Protocol):
    """Backend interface for episodic memory storage."""

    async def append(self, entry: EpisodicEntry) -> None: ...
    async def get_by_session(self, tenant_id: str, session_id: str) -> list[EpisodicEntry]: ...
    async def get_by_user(self, tenant_id: str, user_id: str, limit: int) -> list[EpisodicEntry]: ...
    async def get_by_kind(self, tenant_id: str, kind: EpisodeKind, limit: int) -> list[EpisodicEntry]: ...
    async def search_by_time(
        self, tenant_id: str, start: str, end: str, limit: int,
    ) -> list[EpisodicEntry]: ...
    async def count(self, tenant_id: str) -> int: ...


class PostgresEpisodicBackend:
    """PostgreSQL-backed episodic memory.

    Schema (applied via Alembic migration):

    CREATE TABLE episodic_memory (
        entry_id      TEXT PRIMARY KEY,
        tenant_id     TEXT NOT NULL,
        user_id       TEXT NOT NULL,
        session_id    TEXT NOT NULL,
        kind          TEXT NOT NULL,
        summary       TEXT NOT NULL,
        detail        JSONB DEFAULT '{}',
        actors        TEXT[] DEFAULT '{}',
        outcome       TEXT DEFAULT '',
        duration_ms   INTEGER DEFAULT 0,
        created_at    TIMESTAMPTZ DEFAULT now(),
        embedding_id  TEXT DEFAULT '',
        tags          TEXT[] DEFAULT '{}'
    ) PARTITION BY RANGE (created_at);

    -- Monthly partitions
    CREATE TABLE episodic_memory_2025_01 PARTITION OF episodic_memory
        FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

    -- Indexes
    CREATE INDEX idx_ep_tenant_user ON episodic_memory(tenant_id, user_id, created_at DESC);
    CREATE INDEX idx_ep_session ON episodic_memory(tenant_id, session_id);
    CREATE INDEX idx_ep_kind ON episodic_memory(tenant_id, kind, created_at DESC);
    CREATE INDEX idx_ep_tags ON episodic_memory USING GIN(tags);

    -- RLS
    ALTER TABLE episodic_memory ENABLE ROW LEVEL SECURITY;
    CREATE POLICY tenant_isolation ON episodic_memory
        USING (tenant_id = current_setting('app.tenant_id'));
    """

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def append(self, entry: EpisodicEntry) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO episodic_memory
                    (entry_id, tenant_id, user_id, session_id, kind, summary,
                     detail, actors, outcome, duration_ms, created_at, embedding_id, tags)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
                """,
                entry.entry_id, entry.tenant_id, entry.user_id,
                entry.session_id, entry.kind.value, entry.summary,
                entry.detail, list(entry.actors), entry.outcome,
                entry.duration_ms, entry.created_at, entry.embedding_id,
                list(entry.tags),
            )

    async def get_by_session(self, tenant_id: str, session_id: str) -> list[EpisodicEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM episodic_memory
                WHERE tenant_id = $1 AND session_id = $2
                ORDER BY created_at ASC
                """,
                tenant_id, session_id,
            )
            return [self._row_to_entry(r) for r in rows]

    async def get_by_user(self, tenant_id: str, user_id: str, limit: int) -> list[EpisodicEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM episodic_memory
                WHERE tenant_id = $1 AND user_id = $2
                ORDER BY created_at DESC LIMIT $3
                """,
                tenant_id, user_id, limit,
            )
            return [self._row_to_entry(r) for r in rows]

    async def get_by_kind(self, tenant_id: str, kind: EpisodeKind, limit: int) -> list[EpisodicEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM episodic_memory
                WHERE tenant_id = $1 AND kind = $2
                ORDER BY created_at DESC LIMIT $3
                """,
                tenant_id, kind.value, limit,
            )
            return [self._row_to_entry(r) for r in rows]

    async def search_by_time(
        self, tenant_id: str, start: str, end: str, limit: int,
    ) -> list[EpisodicEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM episodic_memory
                WHERE tenant_id = $1 AND created_at BETWEEN $2 AND $3
                ORDER BY created_at DESC LIMIT $4
                """,
                tenant_id, start, end, limit,
            )
            return [self._row_to_entry(r) for r in rows]

    async def count(self, tenant_id: str) -> int:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT COUNT(*) FROM episodic_memory WHERE tenant_id = $1",
                tenant_id,
            )

    @staticmethod
    def _row_to_entry(row: Any) -> EpisodicEntry:
        return EpisodicEntry(
            entry_id=row["entry_id"],
            tenant_id=row["tenant_id"],
            user_id=row["user_id"],
            session_id=row["session_id"],
            kind=EpisodeKind(row["kind"]),
            summary=row["summary"],
            detail=row["detail"],
            actors=tuple(row["actors"]),
            outcome=row["outcome"],
            duration_ms=row["duration_ms"],
            created_at=str(row["created_at"]),
            embedding_id=row["embedding_id"],
            tags=tuple(row["tags"]),
        )


class EpisodicMemoryManager:
    """Manages the event timeline.

    Every significant interaction is logged as an episode:
    - Conversations (summarized)
    - Tool calls (with inputs/outputs)
    - Errors (with stack traces)
    - Deployments
    - Decisions (with rationale)
    - User feedback
    """

    def __init__(self, config: EpisodicConfig, backend: EpisodicBackend) -> None:
        self._config = config
        self._backend = backend

    async def record(
        self,
        tenant_id: str,
        user_id: str,
        session_id: str,
        kind: EpisodeKind,
        summary: str,
        detail: dict[str, Any] | None = None,
        actors: tuple[str, ...] = (),
        outcome: str = "success",
        duration_ms: int = 0,
        tags: tuple[str, ...] = (),
    ) -> EpisodicEntry:
        """Record an episode."""
        entry = EpisodicEntry(
            tenant_id=tenant_id,
            user_id=user_id,
            session_id=session_id,
            kind=kind,
            summary=summary,
            detail=detail or {},
            actors=actors,
            outcome=outcome,
            duration_ms=duration_ms,
            tags=tags,
        )
        await self._backend.append(entry)
        logger.info("episode_recorded", kind=kind.value, summary=summary[:80])
        return entry

    async def get_user_timeline(
        self, tenant_id: str, user_id: str, limit: int = 50,
    ) -> list[EpisodicEntry]:
        """Get recent episodes for a user."""
        return await self._backend.get_by_user(tenant_id, user_id, limit)

    async def get_session_replay(self, tenant_id: str, session_id: str) -> list[EpisodicEntry]:
        """Replay a session's episodes in order."""
        return await self._backend.get_by_session(tenant_id, session_id)

    async def get_errors(self, tenant_id: str, limit: int = 20) -> list[EpisodicEntry]:
        """Get recent error episodes for debugging."""
        return await self._backend.get_by_kind(tenant_id, EpisodeKind.ERROR, limit)
