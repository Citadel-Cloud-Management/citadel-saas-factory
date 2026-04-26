"""Data models for the 8-layer AI memory architecture.

Each memory layer has its own schema, all immutable (frozen dataclasses).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _uuid() -> str:
    return uuid4().hex[:16]


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class MemoryLayer(str, Enum):
    WORKING = "working"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    ENTITY = "entity"
    SHARED = "shared"


class EntityType(str, Enum):
    USER = "user"
    ORGANIZATION = "organization"
    PRODUCT = "product"
    AGENT = "agent"
    SERVICE = "service"


class EpisodeKind(str, Enum):
    CONVERSATION = "conversation"
    TOOL_CALL = "tool_call"
    ERROR = "error"
    DEPLOYMENT = "deployment"
    DECISION = "decision"
    FEEDBACK = "feedback"


class ProcedureType(str, Enum):
    WORKFLOW = "workflow"
    SKILL = "skill"
    TOOL_PATTERN = "tool_pattern"
    ESCALATION = "escalation"


# ---------------------------------------------------------------------------
# Layer 1: Working Memory
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class WorkingMemoryEntry:
    """Transient context-window tokens. Lives only during a single LLM call."""

    entry_id: str = field(default_factory=_uuid)
    role: str = "system"  # system | user | assistant | tool
    content: str = ""
    token_count: int = 0
    priority: int = 0  # higher = kept longer when truncating
    created_at: str = field(default_factory=_now_iso)


# ---------------------------------------------------------------------------
# Layer 2: Short-Term Memory
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ShortTermEntry:
    """Recent conversation buffer. Persists across turns within a session."""

    entry_id: str = field(default_factory=_uuid)
    session_id: str = ""
    tenant_id: str = ""
    role: str = "user"
    content: str = ""
    summary: str = ""  # compressed version for overflow
    turn_index: int = 0
    token_count: int = 0
    created_at: str = field(default_factory=_now_iso)
    expires_at: str = ""  # ISO timestamp, empty = session-scoped


# ---------------------------------------------------------------------------
# Layer 3: Long-Term Memory
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LongTermEntry:
    """Persistent user data. Survives across sessions."""

    entry_id: str = field(default_factory=_uuid)
    tenant_id: str = ""
    user_id: str = ""
    namespace: str = "general"  # preferences | facts | corrections | feedback
    key: str = ""
    value: Any = None
    confidence: float = 1.0
    source: str = ""  # how was this learned
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    access_count: int = 0
    tags: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Layer 4: Episodic Memory
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EpisodicEntry:
    """Timestamped interaction or event. Append-only log."""

    entry_id: str = field(default_factory=_uuid)
    tenant_id: str = ""
    user_id: str = ""
    session_id: str = ""
    kind: EpisodeKind = EpisodeKind.CONVERSATION
    summary: str = ""
    detail: dict[str, Any] = field(default_factory=dict)
    actors: tuple[str, ...] = field(default_factory=tuple)  # agent IDs involved
    outcome: str = ""  # success | failure | partial
    duration_ms: int = 0
    created_at: str = field(default_factory=_now_iso)
    embedding_id: str = ""  # pointer into vector store for similarity search
    tags: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Layer 5: Semantic Memory (Vector / RAG)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SemanticChunk:
    """Embedded knowledge chunk stored in vector DB."""

    chunk_id: str = field(default_factory=_uuid)
    tenant_id: str = ""
    collection: str = "default"  # namespace within vector DB
    content: str = ""
    source_uri: str = ""  # file path, URL, or document ID
    source_type: str = ""  # pdf | markdown | html | code | transcript
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] = field(default_factory=list)  # populated by embedder
    token_count: int = 0
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)


@dataclass(frozen=True)
class SemanticSearchResult:
    """Result from a vector similarity search."""

    chunk: SemanticChunk
    score: float = 0.0
    rerank_score: float = 0.0


# ---------------------------------------------------------------------------
# Layer 6: Procedural Memory
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProcedureEntry:
    """Learned workflow, skill, or tool-usage pattern."""

    procedure_id: str = field(default_factory=_uuid)
    tenant_id: str = ""
    name: str = ""
    procedure_type: ProcedureType = ProcedureType.WORKFLOW
    description: str = ""
    steps: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    trigger_conditions: tuple[str, ...] = field(default_factory=tuple)
    tools_required: tuple[str, ...] = field(default_factory=tuple)
    success_rate: float = 0.0
    avg_duration_ms: int = 0
    execution_count: int = 0
    last_executed_at: str = ""
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    tags: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Layer 7: Entity Memory
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EntityProfile:
    """Structured profile for a user, org, product, or agent."""

    entity_id: str = field(default_factory=_uuid)
    tenant_id: str = ""
    entity_type: EntityType = EntityType.USER
    name: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)
    relationships: tuple[dict[str, str], ...] = field(default_factory=tuple)
    preferences: dict[str, Any] = field(default_factory=dict)
    history_summary: str = ""
    first_seen_at: str = field(default_factory=_now_iso)
    last_seen_at: str = field(default_factory=_now_iso)
    interaction_count: int = 0
    tags: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Layer 8: Shared Memory (Multi-Agent)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SharedMemoryEntry:
    """Multi-agent coordination state. Concurrency-safe via versioning."""

    entry_id: str = field(default_factory=_uuid)
    tenant_id: str = ""
    namespace: str = "global"  # task-group ID or "global"
    key: str = ""
    value: Any = None
    owner_agent: str = ""  # which agent wrote this
    version: int = 1
    readers: tuple[str, ...] = field(default_factory=tuple)  # agent IDs that consumed
    lock_holder: str = ""  # agent ID holding exclusive write lock, empty = unlocked
    lock_expires_at: str = ""
    created_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    ttl_seconds: int = 0  # 0 = no expiry
