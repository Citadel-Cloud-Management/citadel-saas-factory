"""Configuration for the 8-layer memory system.

All settings are loaded from environment variables with sensible defaults.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class WorkingMemoryConfig:
    max_tokens: int = 128_000  # context window budget
    reserved_tokens: int = 4_096  # always reserved for system prompt
    truncation_strategy: str = "priority"  # priority | fifo | sliding_window


@dataclass(frozen=True)
class ShortTermConfig:
    backend: str = "redis"  # redis | postgres | in_memory
    max_turns: int = 50
    max_tokens_per_session: int = 32_000
    summary_threshold: int = 20  # summarize after N turns
    ttl_seconds: int = 3_600  # 1 hour default session TTL
    redis_prefix: str = "mem:stm:"


@dataclass(frozen=True)
class LongTermConfig:
    backend: str = "postgres"  # postgres | dynamodb | firestore
    table_name: str = "long_term_memory"
    max_entries_per_user: int = 10_000
    decay_enabled: bool = True
    decay_half_life_days: int = 90
    merge_strategy: str = "last_write_wins"  # last_write_wins | confidence_max


@dataclass(frozen=True)
class EpisodicConfig:
    backend: str = "postgres"  # postgres | timescaledb | clickhouse
    table_name: str = "episodic_memory"
    retention_days: int = 365
    partition_by: str = "month"  # day | week | month
    enable_embedding: bool = True


@dataclass(frozen=True)
class SemanticConfig:
    vector_backend: str = "pgvector"  # pgvector | qdrant | pinecone | weaviate
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    chunk_size: int = 512
    chunk_overlap: int = 64
    max_results: int = 10
    similarity_threshold: float = 0.72
    reranker_model: str = "cohere-rerank-v3"
    reranker_enabled: bool = True
    collection_prefix: str = "sem_"


@dataclass(frozen=True)
class ProceduralConfig:
    backend: str = "postgres"
    table_name: str = "procedural_memory"
    auto_learn: bool = True  # learn new procedures from successful interactions
    min_executions_to_learn: int = 3
    success_rate_threshold: float = 0.8


@dataclass(frozen=True)
class EntityConfig:
    backend: str = "postgres"  # postgres | neo4j | neptune
    table_name: str = "entity_profiles"
    graph_enabled: bool = False  # enable graph DB for relationship queries
    graph_backend: str = "neo4j"
    max_relationships_per_entity: int = 500
    auto_extract: bool = True  # extract entities from conversations


@dataclass(frozen=True)
class SharedMemoryConfig:
    backend: str = "redis"  # redis | postgres | etcd
    lock_timeout_seconds: int = 30
    max_lock_retries: int = 3
    conflict_resolution: str = "last_writer_wins"  # last_writer_wins | merge | reject
    broadcast_channel: str = "mem:shared:broadcast"
    redis_prefix: str = "mem:shared:"


@dataclass(frozen=True)
class MemorySystemConfig:
    """Top-level configuration for the entire memory system."""

    working: WorkingMemoryConfig = field(default_factory=WorkingMemoryConfig)
    short_term: ShortTermConfig = field(default_factory=ShortTermConfig)
    long_term: LongTermConfig = field(default_factory=LongTermConfig)
    episodic: EpisodicConfig = field(default_factory=EpisodicConfig)
    semantic: SemanticConfig = field(default_factory=SemanticConfig)
    procedural: ProceduralConfig = field(default_factory=ProceduralConfig)
    entity: EntityConfig = field(default_factory=EntityConfig)
    shared: SharedMemoryConfig = field(default_factory=SharedMemoryConfig)

    # Global settings
    tenant_isolation: bool = True  # enforce RLS on all queries
    encryption_at_rest: bool = True
    audit_all_writes: bool = True
    pii_detection_enabled: bool = True
    max_memory_budget_mb: int = 512  # total in-memory budget


def load_config() -> MemorySystemConfig:
    """Load config from environment variables, falling back to defaults."""
    return MemorySystemConfig(
        working=WorkingMemoryConfig(
            max_tokens=int(os.getenv("MEMORY_WORKING_MAX_TOKENS", "128000")),
        ),
        short_term=ShortTermConfig(
            backend=os.getenv("MEMORY_STM_BACKEND", "redis"),
            max_turns=int(os.getenv("MEMORY_STM_MAX_TURNS", "50")),
            ttl_seconds=int(os.getenv("MEMORY_STM_TTL", "3600")),
        ),
        long_term=LongTermConfig(
            backend=os.getenv("MEMORY_LTM_BACKEND", "postgres"),
        ),
        episodic=EpisodicConfig(
            backend=os.getenv("MEMORY_EPISODIC_BACKEND", "postgres"),
            retention_days=int(os.getenv("MEMORY_EPISODIC_RETENTION_DAYS", "365")),
        ),
        semantic=SemanticConfig(
            vector_backend=os.getenv("MEMORY_VECTOR_BACKEND", "pgvector"),
            embedding_model=os.getenv("MEMORY_EMBEDDING_MODEL", "text-embedding-3-small"),
            embedding_dimensions=int(os.getenv("MEMORY_EMBEDDING_DIM", "1536")),
        ),
        procedural=ProceduralConfig(
            backend=os.getenv("MEMORY_PROCEDURAL_BACKEND", "postgres"),
        ),
        entity=EntityConfig(
            backend=os.getenv("MEMORY_ENTITY_BACKEND", "postgres"),
            graph_enabled=os.getenv("MEMORY_GRAPH_ENABLED", "false").lower() == "true",
        ),
        shared=SharedMemoryConfig(
            backend=os.getenv("MEMORY_SHARED_BACKEND", "redis"),
            lock_timeout_seconds=int(os.getenv("MEMORY_SHARED_LOCK_TIMEOUT", "30")),
        ),
        tenant_isolation=os.getenv("MEMORY_TENANT_ISOLATION", "true").lower() == "true",
        encryption_at_rest=os.getenv("MEMORY_ENCRYPTION", "true").lower() == "true",
        pii_detection_enabled=os.getenv("MEMORY_PII_DETECTION", "true").lower() == "true",
    )
