"""8-Layer AI Memory Architecture for Production SaaS.

Layers:
    1. Working Memory      — context window token management
    2. Short-Term Memory   — recent conversation buffer (Redis)
    3. Long-Term Memory    — persistent user data (PostgreSQL)
    4. Episodic Memory     — timestamped interaction events (PostgreSQL)
    5. Semantic Memory     — vector-based knowledge retrieval / RAG (pgvector)
    6. Procedural Memory   — workflows, skills, tool-usage patterns (PostgreSQL)
    7. Entity Memory       — structured profiles: users, orgs, products (PostgreSQL + Neo4j)
    8. Shared Memory       — multi-agent coordination layer (Redis)

Usage:
    from backbone.memory import MemoryOrchestrator, MemorySystemConfig, load_config

    config = load_config()
    orchestrator = build_orchestrator(config)
    context = await orchestrator.assemble_context(tenant_id, user_id, session_id, query)
"""

from backbone.memory.config import MemorySystemConfig, load_config
from backbone.memory.schemas import (
    EpisodeKind,
    EntityType,
    MemoryLayer,
    ProcedureType,
)
from backbone.memory.orchestrator import MemoryOrchestrator, MemoryContext

__all__ = [
    "MemoryOrchestrator",
    "MemoryContext",
    "MemorySystemConfig",
    "MemoryLayer",
    "EpisodeKind",
    "EntityType",
    "ProcedureType",
    "load_config",
]
