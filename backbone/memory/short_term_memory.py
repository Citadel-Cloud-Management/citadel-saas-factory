"""Layer 2: Short-Term Memory — recent conversation buffer.

Persists across turns within a session. Backed by Redis for low-latency access.
Supports automatic summarization when turn count exceeds threshold.
"""

from __future__ import annotations

import json
from dataclasses import replace
from typing import Any, Protocol

import structlog

from backbone.memory.config import ShortTermConfig
from backbone.memory.schemas import ShortTermEntry

logger = structlog.get_logger("memory.short_term")


class ShortTermBackend(Protocol):
    """Backend interface for short-term memory storage."""

    async def get_session(self, tenant_id: str, session_id: str) -> list[ShortTermEntry]: ...
    async def append(self, entry: ShortTermEntry) -> None: ...
    async def get_recent(self, tenant_id: str, session_id: str, limit: int) -> list[ShortTermEntry]: ...
    async def clear_session(self, tenant_id: str, session_id: str) -> int: ...
    async def set_ttl(self, tenant_id: str, session_id: str, ttl_seconds: int) -> None: ...


class RedisShortTermBackend:
    """Redis-backed short-term memory."""

    def __init__(self, redis_client: Any, prefix: str = "mem:stm:") -> None:
        self._redis = redis_client
        self._prefix = prefix

    def _key(self, tenant_id: str, session_id: str) -> str:
        return f"{self._prefix}{tenant_id}:{session_id}"

    async def get_session(self, tenant_id: str, session_id: str) -> list[ShortTermEntry]:
        key = self._key(tenant_id, session_id)
        raw_entries = await self._redis.lrange(key, 0, -1)
        return [self._deserialize(e) for e in raw_entries]

    async def append(self, entry: ShortTermEntry) -> None:
        key = self._key(entry.tenant_id, entry.session_id)
        await self._redis.rpush(key, self._serialize(entry))
        logger.debug("stm_appended", session=entry.session_id, turn=entry.turn_index)

    async def get_recent(self, tenant_id: str, session_id: str, limit: int) -> list[ShortTermEntry]:
        key = self._key(tenant_id, session_id)
        raw_entries = await self._redis.lrange(key, -limit, -1)
        return [self._deserialize(e) for e in raw_entries]

    async def clear_session(self, tenant_id: str, session_id: str) -> int:
        key = self._key(tenant_id, session_id)
        length = await self._redis.llen(key)
        await self._redis.delete(key)
        return length

    async def set_ttl(self, tenant_id: str, session_id: str, ttl_seconds: int) -> None:
        key = self._key(tenant_id, session_id)
        await self._redis.expire(key, ttl_seconds)

    @staticmethod
    def _serialize(entry: ShortTermEntry) -> str:
        return json.dumps({
            "entry_id": entry.entry_id,
            "session_id": entry.session_id,
            "tenant_id": entry.tenant_id,
            "role": entry.role,
            "content": entry.content,
            "summary": entry.summary,
            "turn_index": entry.turn_index,
            "token_count": entry.token_count,
            "created_at": entry.created_at,
            "expires_at": entry.expires_at,
        })

    @staticmethod
    def _deserialize(raw: str | bytes) -> ShortTermEntry:
        data = json.loads(raw)
        return ShortTermEntry(**data)


class InMemoryShortTermBackend:
    """In-memory backend for testing and development."""

    def __init__(self) -> None:
        self._store: dict[str, list[ShortTermEntry]] = {}

    def _key(self, tenant_id: str, session_id: str) -> str:
        return f"{tenant_id}:{session_id}"

    async def get_session(self, tenant_id: str, session_id: str) -> list[ShortTermEntry]:
        return list(self._store.get(self._key(tenant_id, session_id), []))

    async def append(self, entry: ShortTermEntry) -> None:
        key = self._key(entry.tenant_id, entry.session_id)
        if key not in self._store:
            self._store[key] = []
        self._store[key].append(entry)

    async def get_recent(self, tenant_id: str, session_id: str, limit: int) -> list[ShortTermEntry]:
        entries = self._store.get(self._key(tenant_id, session_id), [])
        return list(entries[-limit:])

    async def clear_session(self, tenant_id: str, session_id: str) -> int:
        key = self._key(tenant_id, session_id)
        count = len(self._store.get(key, []))
        self._store.pop(key, None)
        return count

    async def set_ttl(self, tenant_id: str, session_id: str, ttl_seconds: int) -> None:
        pass  # no-op for in-memory


class ShortTermMemoryManager:
    """Manages conversation buffers across sessions.

    Features:
    - Append new turns
    - Auto-summarize when threshold exceeded
    - TTL-based expiry
    - Session isolation per tenant
    """

    def __init__(self, config: ShortTermConfig, backend: ShortTermBackend) -> None:
        self._config = config
        self._backend = backend

    async def add_turn(
        self,
        tenant_id: str,
        session_id: str,
        role: str,
        content: str,
        token_count: int = 0,
    ) -> ShortTermEntry:
        """Add a conversation turn to the session buffer."""
        existing = await self._backend.get_session(tenant_id, session_id)
        turn_index = len(existing)

        entry = ShortTermEntry(
            session_id=session_id,
            tenant_id=tenant_id,
            role=role,
            content=content,
            turn_index=turn_index,
            token_count=token_count,
        )
        await self._backend.append(entry)
        await self._backend.set_ttl(tenant_id, session_id, self._config.ttl_seconds)

        if turn_index >= self._config.summary_threshold:
            logger.info("stm_summary_needed", session=session_id, turns=turn_index)

        return entry

    async def get_context(self, tenant_id: str, session_id: str, max_turns: int | None = None) -> list[ShortTermEntry]:
        """Get recent conversation context for injection into working memory."""
        limit = max_turns or self._config.max_turns
        return await self._backend.get_recent(tenant_id, session_id, limit)

    async def clear(self, tenant_id: str, session_id: str) -> int:
        """Clear a session's short-term memory."""
        return await self._backend.clear_session(tenant_id, session_id)
