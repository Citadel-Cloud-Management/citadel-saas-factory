"""Layer 8: Shared Memory — multi-agent coordination layer.

Redis-backed shared state with distributed locking, versioning,
and pub/sub broadcast for agent-to-agent communication.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from typing import Any, Protocol

import structlog

from backbone.memory.config import SharedMemoryConfig
from backbone.memory.schemas import SharedMemoryEntry, _now_iso

logger = structlog.get_logger("memory.shared")


class SharedMemoryBackend(Protocol):
    """Backend interface for shared memory."""

    async def get(self, tenant_id: str, namespace: str, key: str) -> SharedMemoryEntry | None: ...
    async def set(self, entry: SharedMemoryEntry) -> bool: ...
    async def compare_and_set(self, entry: SharedMemoryEntry, expected_version: int) -> bool: ...
    async def delete(self, tenant_id: str, namespace: str, key: str) -> bool: ...
    async def list_namespace(self, tenant_id: str, namespace: str) -> list[SharedMemoryEntry]: ...
    async def acquire_lock(self, tenant_id: str, namespace: str, key: str, agent_id: str, ttl: int) -> bool: ...
    async def release_lock(self, tenant_id: str, namespace: str, key: str, agent_id: str) -> bool: ...
    async def publish(self, channel: str, message: str) -> None: ...
    async def subscribe(self, channel: str) -> Any: ...


class RedisSharedMemoryBackend:
    """Redis-backed shared memory with distributed locking."""

    def __init__(self, redis_client: Any, prefix: str = "mem:shared:") -> None:
        self._redis = redis_client
        self._prefix = prefix

    def _key(self, tenant_id: str, namespace: str, key: str) -> str:
        return f"{self._prefix}{tenant_id}:{namespace}:{key}"

    def _lock_key(self, tenant_id: str, namespace: str, key: str) -> str:
        return f"{self._prefix}lock:{tenant_id}:{namespace}:{key}"

    async def get(self, tenant_id: str, namespace: str, key: str) -> SharedMemoryEntry | None:
        raw = await self._redis.get(self._key(tenant_id, namespace, key))
        if not raw:
            return None
        return self._deserialize(raw)

    async def set(self, entry: SharedMemoryEntry) -> bool:
        k = self._key(entry.tenant_id, entry.namespace, entry.key)
        data = self._serialize(entry)
        if entry.ttl_seconds > 0:
            await self._redis.setex(k, entry.ttl_seconds, data)
        else:
            await self._redis.set(k, data)
        return True

    async def compare_and_set(self, entry: SharedMemoryEntry, expected_version: int) -> bool:
        """Optimistic concurrency: only write if version matches."""
        k = self._key(entry.tenant_id, entry.namespace, entry.key)
        raw = await self._redis.get(k)
        if raw:
            existing = self._deserialize(raw)
            if existing.version != expected_version:
                return False
        data = self._serialize(entry)
        if entry.ttl_seconds > 0:
            await self._redis.setex(k, entry.ttl_seconds, data)
        else:
            await self._redis.set(k, data)
        return True

    async def delete(self, tenant_id: str, namespace: str, key: str) -> bool:
        return bool(await self._redis.delete(self._key(tenant_id, namespace, key)))

    async def list_namespace(self, tenant_id: str, namespace: str) -> list[SharedMemoryEntry]:
        pattern = f"{self._prefix}{tenant_id}:{namespace}:*"
        keys = []
        async for key in self._redis.scan_iter(match=pattern, count=100):
            keys.append(key)
        entries = []
        for key in keys:
            raw = await self._redis.get(key)
            if raw:
                entries.append(self._deserialize(raw))
        return entries

    async def acquire_lock(self, tenant_id: str, namespace: str, key: str, agent_id: str, ttl: int) -> bool:
        lock_key = self._lock_key(tenant_id, namespace, key)
        acquired = await self._redis.set(lock_key, agent_id, nx=True, ex=ttl)
        return bool(acquired)

    async def release_lock(self, tenant_id: str, namespace: str, key: str, agent_id: str) -> bool:
        lock_key = self._lock_key(tenant_id, namespace, key)
        current = await self._redis.get(lock_key)
        if current and current.decode() == agent_id:
            await self._redis.delete(lock_key)
            return True
        return False

    async def publish(self, channel: str, message: str) -> None:
        await self._redis.publish(channel, message)

    async def subscribe(self, channel: str) -> Any:
        pubsub = self._redis.pubsub()
        await pubsub.subscribe(channel)
        return pubsub

    @staticmethod
    def _serialize(entry: SharedMemoryEntry) -> str:
        return json.dumps({
            "entry_id": entry.entry_id,
            "tenant_id": entry.tenant_id,
            "namespace": entry.namespace,
            "key": entry.key,
            "value": entry.value,
            "owner_agent": entry.owner_agent,
            "version": entry.version,
            "readers": list(entry.readers),
            "lock_holder": entry.lock_holder,
            "lock_expires_at": entry.lock_expires_at,
            "created_at": entry.created_at,
            "updated_at": entry.updated_at,
            "ttl_seconds": entry.ttl_seconds,
        })

    @staticmethod
    def _deserialize(raw: str | bytes) -> SharedMemoryEntry:
        data = json.loads(raw)
        return SharedMemoryEntry(
            entry_id=data["entry_id"],
            tenant_id=data["tenant_id"],
            namespace=data["namespace"],
            key=data["key"],
            value=data["value"],
            owner_agent=data["owner_agent"],
            version=data["version"],
            readers=tuple(data.get("readers", [])),
            lock_holder=data.get("lock_holder", ""),
            lock_expires_at=data.get("lock_expires_at", ""),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            ttl_seconds=data.get("ttl_seconds", 0),
        )


class SharedMemoryManager:
    """Manages multi-agent coordination state.

    Provides:
    - Shared key-value store with namespace isolation
    - Distributed locking for exclusive access
    - Optimistic concurrency via version checks
    - Pub/sub broadcast for agent notifications
    - Conflict resolution strategies
    """

    def __init__(self, config: SharedMemoryConfig, backend: SharedMemoryBackend) -> None:
        self._config = config
        self._backend = backend

    async def write(
        self,
        tenant_id: str,
        namespace: str,
        key: str,
        value: Any,
        agent_id: str,
        ttl_seconds: int = 0,
    ) -> SharedMemoryEntry:
        """Write to shared memory. Auto-increments version."""
        existing = await self._backend.get(tenant_id, namespace, key)
        version = (existing.version + 1) if existing else 1

        entry = SharedMemoryEntry(
            tenant_id=tenant_id,
            namespace=namespace,
            key=key,
            value=value,
            owner_agent=agent_id,
            version=version,
            ttl_seconds=ttl_seconds,
        )
        await self._backend.set(entry)
        logger.debug("shared_write", key=key, agent=agent_id, version=version)
        return entry

    async def read(self, tenant_id: str, namespace: str, key: str, agent_id: str = "") -> SharedMemoryEntry | None:
        """Read from shared memory. Optionally track which agent read it."""
        entry = await self._backend.get(tenant_id, namespace, key)
        if entry and agent_id and agent_id not in entry.readers:
            updated = SharedMemoryEntry(
                entry_id=entry.entry_id,
                tenant_id=entry.tenant_id,
                namespace=entry.namespace,
                key=entry.key,
                value=entry.value,
                owner_agent=entry.owner_agent,
                version=entry.version,
                readers=(*entry.readers, agent_id),
                lock_holder=entry.lock_holder,
                lock_expires_at=entry.lock_expires_at,
                created_at=entry.created_at,
                updated_at=entry.updated_at,
                ttl_seconds=entry.ttl_seconds,
            )
            await self._backend.set(updated)
        return entry

    async def write_exclusive(
        self,
        tenant_id: str,
        namespace: str,
        key: str,
        value: Any,
        agent_id: str,
        ttl_seconds: int = 0,
    ) -> SharedMemoryEntry | None:
        """Write with distributed lock. Returns None if lock not acquired."""
        lock_acquired = await self._backend.acquire_lock(
            tenant_id, namespace, key, agent_id,
            self._config.lock_timeout_seconds,
        )
        if not lock_acquired:
            logger.warning("shared_lock_failed", key=key, agent=agent_id)
            return None

        try:
            entry = await self.write(tenant_id, namespace, key, value, agent_id, ttl_seconds)
            return entry
        finally:
            await self._backend.release_lock(tenant_id, namespace, key, agent_id)

    async def broadcast(self, tenant_id: str, event: str, data: dict[str, Any], agent_id: str) -> None:
        """Broadcast an event to all listening agents."""
        message = json.dumps({
            "tenant_id": tenant_id,
            "event": event,
            "data": data,
            "agent_id": agent_id,
            "timestamp": _now_iso(),
        })
        await self._backend.publish(self._config.broadcast_channel, message)
        logger.debug("shared_broadcast", event=event, agent=agent_id)

    async def list_namespace(self, tenant_id: str, namespace: str) -> list[SharedMemoryEntry]:
        """List all entries in a namespace."""
        return await self._backend.list_namespace(tenant_id, namespace)
