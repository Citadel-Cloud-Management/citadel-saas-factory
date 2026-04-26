"""Memory Orchestrator — middleware that coordinates all 8 memory layers.

This is the single entry point for all memory operations during an LLM call.
It assembles context from all layers, manages writes back after inference,
and handles the personalization pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import structlog

from backbone.memory.config import MemorySystemConfig
from backbone.memory.schemas import (
    EpisodeKind,
    MemoryLayer,
    SemanticSearchResult,
    WorkingMemoryEntry,
)
from backbone.memory.working_memory import WorkingMemoryManager, WorkingMemoryState
from backbone.memory.short_term_memory import ShortTermMemoryManager
from backbone.memory.long_term_memory import LongTermMemoryManager
from backbone.memory.episodic_memory import EpisodicMemoryManager
from backbone.memory.semantic_memory import SemanticMemoryManager
from backbone.memory.procedural_memory import ProceduralMemoryManager
from backbone.memory.entity_memory import EntityMemoryManager
from backbone.memory.shared_memory import SharedMemoryManager

logger = structlog.get_logger("memory.orchestrator")


@dataclass(frozen=True)
class MemoryContext:
    """Assembled context from all memory layers for a single LLM call."""

    working_messages: list[dict[str, str]] = field(default_factory=list)
    short_term_turns: list[dict[str, str]] = field(default_factory=list)
    long_term_facts: dict[str, Any] = field(default_factory=dict)
    relevant_episodes: list[dict[str, Any]] = field(default_factory=list)
    semantic_chunks: list[dict[str, Any]] = field(default_factory=list)
    applicable_procedures: list[dict[str, Any]] = field(default_factory=list)
    entity_profile: dict[str, Any] = field(default_factory=dict)
    shared_state: dict[str, Any] = field(default_factory=dict)
    total_tokens_used: int = 0


class MemoryOrchestrator:
    """Coordinates all 8 memory layers for LLM calls.

    Lifecycle per request:

    1. PRE-INFERENCE: assemble context
       - Load working memory (system prompt, injections)
       - Load short-term memory (recent conversation turns)
       - Query long-term memory (user preferences, facts)
       - Query episodic memory (relevant past interactions)
       - Query semantic memory (RAG retrieval)
       - Query procedural memory (applicable workflows)
       - Load entity profile (user/org context)
       - Load shared memory (multi-agent state)
       - Budget and truncate to fit context window

    2. INFERENCE: pass assembled context to LLM

    3. POST-INFERENCE: write back
       - Append to short-term memory
       - Update long-term memory (new facts learned)
       - Record episode
       - Update entity profile (interaction count, new attributes)
       - Update shared memory (if multi-agent)
       - Update procedural memory (if workflow completed)
    """

    def __init__(
        self,
        config: MemorySystemConfig,
        working: WorkingMemoryManager,
        short_term: ShortTermMemoryManager,
        long_term: LongTermMemoryManager,
        episodic: EpisodicMemoryManager,
        semantic: SemanticMemoryManager,
        procedural: ProceduralMemoryManager,
        entity: EntityMemoryManager,
        shared: SharedMemoryManager,
    ) -> None:
        self._config = config
        self._working = working
        self._short_term = short_term
        self._long_term = long_term
        self._episodic = episodic
        self._semantic = semantic
        self._procedural = procedural
        self._entity = entity
        self._shared = shared

    async def assemble_context(
        self,
        tenant_id: str,
        user_id: str,
        session_id: str,
        query: str,
        system_prompt: str = "",
        agent_id: str = "",
        semantic_collection: str = "default",
    ) -> MemoryContext:
        """Assemble full context from all 8 memory layers.

        This is the main entry point called before every LLM invocation.
        Returns a MemoryContext with all relevant information, budgeted
        to fit within the context window.
        """
        state = self._working.create_state()

        # Layer 1: Working memory — system prompt
        if system_prompt:
            state = self._working.add_entry(state, WorkingMemoryEntry(
                role="system",
                content=system_prompt,
                token_count=len(system_prompt.split()),
                priority=100,
            ))

        # Layer 7: Entity profile — inject user context early
        entity_data = await self._entity.get_with_relationships(tenant_id, user_id)
        entity_context = ""
        if entity_data and entity_data.get("profile"):
            profile = entity_data["profile"]
            entity_context = self._format_entity_context(profile, entity_data.get("relationships", []))
            state = self._working.add_entry(state, WorkingMemoryEntry(
                role="system",
                content=entity_context,
                token_count=len(entity_context.split()),
                priority=80,
            ))

        # Layer 3: Long-term memory — user preferences and facts
        user_memories = await self._long_term.get_user_profile(tenant_id, user_id)
        ltm_context = self._format_long_term_context(user_memories)
        if ltm_context:
            state = self._working.add_entry(state, WorkingMemoryEntry(
                role="system",
                content=ltm_context,
                token_count=len(ltm_context.split()),
                priority=70,
            ))

        # Layer 5: Semantic memory — RAG retrieval
        semantic_results = await self._semantic.search(
            tenant_id, query, collection=semantic_collection,
        )
        if semantic_results:
            rag_context = self._format_semantic_context(semantic_results)
            state = self._working.add_entry(state, WorkingMemoryEntry(
                role="system",
                content=rag_context,
                token_count=len(rag_context.split()),
                priority=60,
            ))

        # Layer 6: Procedural memory — applicable workflows
        procedures = await self._procedural.find_applicable(tenant_id, query)
        proc_context = ""
        if procedures:
            proc_context = self._format_procedural_context(procedures)
            state = self._working.add_entry(state, WorkingMemoryEntry(
                role="system",
                content=proc_context,
                token_count=len(proc_context.split()),
                priority=50,
            ))

        # Layer 4: Episodic memory — relevant past interactions
        recent_episodes = await self._episodic.get_user_timeline(tenant_id, user_id, limit=10)
        ep_context = ""
        if recent_episodes:
            ep_context = self._format_episodic_context(recent_episodes)
            state = self._working.add_entry(state, WorkingMemoryEntry(
                role="system",
                content=ep_context,
                token_count=len(ep_context.split()),
                priority=40,
            ))

        # Layer 8: Shared memory — multi-agent state
        shared_entries = []
        shared_context = ""
        if agent_id:
            shared_entries = await self._shared.list_namespace(tenant_id, "global")
            if shared_entries:
                shared_context = self._format_shared_context(shared_entries)
                state = self._working.add_entry(state, WorkingMemoryEntry(
                    role="system",
                    content=shared_context,
                    token_count=len(shared_context.split()),
                    priority=30,
                ))

        # Layer 2: Short-term memory — recent conversation turns
        recent_turns = await self._short_term.get_context(tenant_id, session_id)
        for turn in recent_turns:
            state = self._working.add_entry(state, WorkingMemoryEntry(
                role=turn.role,
                content=turn.content,
                token_count=turn.token_count,
                priority=90,  # conversation history is high priority
            ))

        # Add current query
        state = self._working.add_entry(state, WorkingMemoryEntry(
            role="user",
            content=query,
            token_count=len(query.split()),
            priority=100,
        ))

        # Truncate to fit context window
        messages = self._working.build_messages(state)

        logger.info(
            "context_assembled",
            layers_active=sum([
                1, bool(recent_turns), bool(user_memories),
                bool(recent_episodes), bool(semantic_results),
                bool(procedures), bool(entity_data), bool(shared_entries),
            ]),
            total_entries=len(state.entries),
            total_tokens=state.total_tokens,
        )

        return MemoryContext(
            working_messages=messages,
            short_term_turns=[{"role": t.role, "content": t.content} for t in recent_turns],
            long_term_facts={ns: [{"key": e.key, "value": e.value} for e in entries]
                            for ns, entries in user_memories.items()},
            relevant_episodes=[{"summary": e.summary, "kind": e.kind.value} for e in recent_episodes],
            semantic_chunks=[{"content": r.chunk.content, "score": r.score} for r in semantic_results],
            applicable_procedures=[{"name": p.name, "steps": list(p.steps)} for p in procedures],
            entity_profile=entity_data,
            shared_state={e.key: e.value for e in shared_entries},
            total_tokens_used=state.total_tokens,
        )

    async def post_inference(
        self,
        tenant_id: str,
        user_id: str,
        session_id: str,
        user_message: str,
        assistant_response: str,
        agent_id: str = "",
        duration_ms: int = 0,
    ) -> None:
        """Write back to memory layers after LLM inference.

        Called after every successful LLM response.
        """
        # Layer 2: Append to short-term memory
        await self._short_term.add_turn(
            tenant_id, session_id, "user", user_message,
            token_count=len(user_message.split()),
        )
        await self._short_term.add_turn(
            tenant_id, session_id, "assistant", assistant_response,
            token_count=len(assistant_response.split()),
        )

        # Layer 4: Record episode
        await self._episodic.record(
            tenant_id=tenant_id,
            user_id=user_id,
            session_id=session_id,
            kind=EpisodeKind.CONVERSATION,
            summary=user_message[:200],
            detail={"response_length": len(assistant_response)},
            actors=(agent_id,) if agent_id else (),
            outcome="success",
            duration_ms=duration_ms,
        )

        logger.debug("post_inference_complete", session=session_id)

    # -----------------------------------------------------------------------
    # Context formatters (private)
    # -----------------------------------------------------------------------

    @staticmethod
    def _format_entity_context(profile: Any, relationships: list[dict]) -> str:
        lines = [f"[User Profile] Name: {profile.name}"]
        if hasattr(profile, "attributes") and profile.attributes:
            for k, v in profile.attributes.items():
                lines.append(f"  {k}: {v}")
        if hasattr(profile, "preferences") and profile.preferences:
            lines.append("Preferences:")
            for k, v in profile.preferences.items():
                lines.append(f"  {k}: {v}")
        if relationships:
            lines.append("Relationships:")
            for r in relationships[:10]:
                lines.append(f"  {r.get('relation', '')}: {r.get('name', '')}")
        return "\n".join(lines)

    @staticmethod
    def _format_long_term_context(memories: dict[str, list]) -> str:
        if not memories:
            return ""
        lines = ["[User Memory]"]
        for namespace, entries in memories.items():
            for entry in entries[:10]:
                lines.append(f"  [{namespace}] {entry.key}: {entry.value}")
        return "\n".join(lines)

    @staticmethod
    def _format_semantic_context(results: list[SemanticSearchResult]) -> str:
        lines = ["[Relevant Knowledge]"]
        for r in results[:5]:
            lines.append(f"  (score: {r.score:.2f}) {r.chunk.content[:500]}")
        return "\n".join(lines)

    @staticmethod
    def _format_procedural_context(procedures: list) -> str:
        lines = ["[Available Procedures]"]
        for p in procedures[:3]:
            lines.append(f"  {p.name}: {p.description}")
        return "\n".join(lines)

    @staticmethod
    def _format_episodic_context(episodes: list) -> str:
        lines = ["[Recent History]"]
        for ep in episodes[:5]:
            lines.append(f"  [{ep.kind.value}] {ep.summary[:100]}")
        return "\n".join(lines)

    @staticmethod
    def _format_shared_context(entries: list) -> str:
        lines = ["[Shared Agent State]"]
        for e in entries[:10]:
            lines.append(f"  {e.key}: {e.value}")
        return "\n".join(lines)
