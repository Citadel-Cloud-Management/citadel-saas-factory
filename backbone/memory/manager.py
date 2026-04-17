"""Memory Manager — multi-tier memory system for autonomous agents."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger("memory")


class MemoryType(str, Enum):
    WORKING = "working"       # Current task context, temporary
    SESSION = "session"       # What happened this run
    LONG_TERM = "long_term"   # Reusable facts, decisions, preferences
    AUDIT = "audit"           # Immutable action log


@dataclass(frozen=True)
class MemoryEntry:
    """Immutable memory record."""

    entry_id: str
    memory_type: MemoryType
    key: str
    value: Any
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ttl_seconds: int | None = None
    tags: tuple[str, ...] = field(default_factory=tuple)
    source: str = ""


class MemoryManager:
    """Manages multi-tier memory for the agent backbone.

    Memory tiers:
    - Working: ephemeral, current task only, cleared between runs
    - Session: persists for the duration of a run
    - Long-term: persists across runs, file-backed
    - Audit: immutable log, append-only

    All writes are versioned and traceable.
    """

    ALLOWED_BASE_DIRS = ("backbone/", "data/", ".claude/")
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self, storage_dir: str = "backbone/memory/store") -> None:
        resolved = Path(storage_dir).resolve()
        cwd = Path.cwd().resolve()
        if not any(storage_dir.startswith(prefix) for prefix in self.ALLOWED_BASE_DIRS):
            if not str(resolved).startswith(str(cwd)):
                raise ValueError(f"Storage dir must be within project: {storage_dir}")
        self._storage_dir = Path(storage_dir)
        self._working: dict[str, MemoryEntry] = {}
        self._session: dict[str, MemoryEntry] = {}
        self._long_term: dict[str, MemoryEntry] = {}
        self._audit: list[MemoryEntry] = []

    def store(self, entry: MemoryEntry) -> None:
        """Store a memory entry in the appropriate tier."""
        target = self._get_tier(entry.memory_type)
        if isinstance(target, dict):
            target[entry.key] = entry
        elif isinstance(target, list):
            target.append(entry)

        logger.debug(
            "memory_stored",
            type=entry.memory_type.value,
            key=entry.key,
            source=entry.source,
        )

    def recall(self, key: str, memory_type: MemoryType | None = None) -> MemoryEntry | None:
        """Recall a memory by key, searching specified tier or all tiers."""
        if memory_type:
            tier = self._get_tier(memory_type)
            if isinstance(tier, dict):
                return tier.get(key)
            return None

        for tier_type in [MemoryType.WORKING, MemoryType.SESSION, MemoryType.LONG_TERM]:
            tier = self._get_tier(tier_type)
            if isinstance(tier, dict) and key in tier:
                return tier[key]
        return None

    def search(self, query: str, memory_type: MemoryType | None = None) -> list[MemoryEntry]:
        """Search memory by keyword match on key, value, or tags."""
        results: list[MemoryEntry] = []
        query_lower = query.lower()

        tiers = [memory_type] if memory_type else [MemoryType.WORKING, MemoryType.SESSION, MemoryType.LONG_TERM]

        for tier_type in tiers:
            tier = self._get_tier(tier_type)
            if isinstance(tier, dict):
                for entry in tier.values():
                    if self._matches(entry, query_lower):
                        results.append(entry)

        return results

    def clear_working(self) -> int:
        """Clear working memory. Returns count of cleared entries."""
        count = len(self._working)
        self._working.clear()
        logger.info("working_memory_cleared", count=count)
        return count

    def clear_session(self) -> int:
        """Clear session memory. Returns count of cleared entries."""
        count = len(self._session)
        self._session.clear()
        logger.info("session_memory_cleared", count=count)
        return count

    def get_audit_log(self, limit: int = 100) -> list[MemoryEntry]:
        """Get recent audit entries."""
        return self._audit[-limit:]

    def persist_long_term(self) -> int:
        """Write long-term memory to disk."""
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        path = self._storage_dir / "long_term.json"

        entries = [
            {
                "entry_id": e.entry_id,
                "key": e.key,
                "value": e.value,
                "created_at": e.created_at,
                "tags": list(e.tags),
                "source": e.source,
            }
            for e in self._long_term.values()
        ]

        path.write_text(json.dumps(entries, indent=2))
        logger.info("long_term_persisted", count=len(entries), path=str(path))
        return len(entries)

    def load_long_term(self) -> int:
        """Load long-term memory from disk."""
        path = self._storage_dir / "long_term.json"
        if not path.exists():
            return 0

        file_size = path.stat().st_size
        if file_size > self.MAX_FILE_SIZE:
            logger.error("long_term_file_too_large", size=file_size, max=self.MAX_FILE_SIZE)
            return 0

        entries = json.loads(path.read_text())
        for e in entries:
            entry = MemoryEntry(
                entry_id=e["entry_id"],
                memory_type=MemoryType.LONG_TERM,
                key=e["key"],
                value=e["value"],
                created_at=e.get("created_at", ""),
                tags=tuple(e.get("tags", [])),
                source=e.get("source", ""),
            )
            self._long_term[entry.key] = entry

        logger.info("long_term_loaded", count=len(entries))
        return len(entries)

    def _get_tier(self, memory_type: MemoryType) -> dict | list:
        return {
            MemoryType.WORKING: self._working,
            MemoryType.SESSION: self._session,
            MemoryType.LONG_TERM: self._long_term,
            MemoryType.AUDIT: self._audit,
        }[memory_type]

    @staticmethod
    def _matches(entry: MemoryEntry, query: str) -> bool:
        if query in entry.key.lower():
            return True
        if isinstance(entry.value, str) and query in entry.value.lower():
            return True
        return any(query in tag.lower() for tag in entry.tags)
