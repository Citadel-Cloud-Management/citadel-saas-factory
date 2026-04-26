"""Layer 6: Procedural Memory — workflows, skills, and tool-usage patterns.

Stores learned sequences of actions that agents have successfully executed.
Enables agents to recall "how to do things" rather than "what things are."
"""

from __future__ import annotations

from typing import Any, Protocol

import structlog

from backbone.memory.config import ProceduralConfig
from backbone.memory.schemas import ProcedureEntry, ProcedureType

logger = structlog.get_logger("memory.procedural")


class ProceduralBackend(Protocol):
    """Backend interface for procedural memory."""

    async def upsert(self, entry: ProcedureEntry) -> None: ...
    async def get(self, tenant_id: str, procedure_id: str) -> ProcedureEntry | None: ...
    async def find_by_trigger(self, tenant_id: str, context: str) -> list[ProcedureEntry]: ...
    async def find_by_type(self, tenant_id: str, proc_type: ProcedureType) -> list[ProcedureEntry]: ...
    async def find_by_tools(self, tenant_id: str, tools: list[str]) -> list[ProcedureEntry]: ...
    async def update_stats(self, procedure_id: str, success: bool, duration_ms: int) -> None: ...
    async def list_all(self, tenant_id: str, limit: int) -> list[ProcedureEntry]: ...


class PostgresProceduralBackend:
    """PostgreSQL-backed procedural memory.

    Schema:

    CREATE TABLE procedural_memory (
        procedure_id        TEXT PRIMARY KEY,
        tenant_id           TEXT NOT NULL,
        name                TEXT NOT NULL,
        procedure_type      TEXT NOT NULL,
        description         TEXT DEFAULT '',
        steps               JSONB NOT NULL DEFAULT '[]',
        trigger_conditions  TEXT[] DEFAULT '{}',
        tools_required      TEXT[] DEFAULT '{}',
        success_rate        REAL DEFAULT 0.0,
        avg_duration_ms     INTEGER DEFAULT 0,
        execution_count     INTEGER DEFAULT 0,
        last_executed_at    TIMESTAMPTZ,
        created_at          TIMESTAMPTZ DEFAULT now(),
        updated_at          TIMESTAMPTZ DEFAULT now(),
        tags                TEXT[] DEFAULT '{}'
    );

    CREATE INDEX idx_proc_tenant ON procedural_memory(tenant_id);
    CREATE INDEX idx_proc_type ON procedural_memory(tenant_id, procedure_type);
    CREATE INDEX idx_proc_tools ON procedural_memory USING GIN(tools_required);
    CREATE INDEX idx_proc_triggers ON procedural_memory USING GIN(trigger_conditions);
    """

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def upsert(self, entry: ProcedureEntry) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO procedural_memory
                    (procedure_id, tenant_id, name, procedure_type, description,
                     steps, trigger_conditions, tools_required, success_rate,
                     avg_duration_ms, execution_count, last_executed_at,
                     created_at, updated_at, tags)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)
                ON CONFLICT (procedure_id) DO UPDATE SET
                    steps = EXCLUDED.steps,
                    description = EXCLUDED.description,
                    updated_at = now()
                """,
                entry.procedure_id, entry.tenant_id, entry.name,
                entry.procedure_type.value, entry.description,
                list(entry.steps), list(entry.trigger_conditions),
                list(entry.tools_required), entry.success_rate,
                entry.avg_duration_ms, entry.execution_count,
                entry.last_executed_at or None,
                entry.created_at, entry.updated_at, list(entry.tags),
            )

    async def get(self, tenant_id: str, procedure_id: str) -> ProcedureEntry | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM procedural_memory WHERE tenant_id = $1 AND procedure_id = $2",
                tenant_id, procedure_id,
            )
            return self._row_to_entry(row) if row else None

    async def find_by_trigger(self, tenant_id: str, context: str) -> list[ProcedureEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM procedural_memory
                WHERE tenant_id = $1 AND trigger_conditions && ARRAY[$2]
                ORDER BY success_rate DESC, execution_count DESC
                """,
                tenant_id, context,
            )
            return [self._row_to_entry(r) for r in rows]

    async def find_by_type(self, tenant_id: str, proc_type: ProcedureType) -> list[ProcedureEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM procedural_memory
                WHERE tenant_id = $1 AND procedure_type = $2
                ORDER BY execution_count DESC
                """,
                tenant_id, proc_type.value,
            )
            return [self._row_to_entry(r) for r in rows]

    async def find_by_tools(self, tenant_id: str, tools: list[str]) -> list[ProcedureEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM procedural_memory
                WHERE tenant_id = $1 AND tools_required && $2
                ORDER BY success_rate DESC
                """,
                tenant_id, tools,
            )
            return [self._row_to_entry(r) for r in rows]

    async def update_stats(self, procedure_id: str, success: bool, duration_ms: int) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE procedural_memory SET
                    execution_count = execution_count + 1,
                    success_rate = (success_rate * execution_count + $2) / (execution_count + 1),
                    avg_duration_ms = (avg_duration_ms * execution_count + $3) / (execution_count + 1),
                    last_executed_at = now(),
                    updated_at = now()
                WHERE procedure_id = $1
                """,
                procedure_id, 1.0 if success else 0.0, duration_ms,
            )

    async def list_all(self, tenant_id: str, limit: int) -> list[ProcedureEntry]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM procedural_memory WHERE tenant_id = $1 ORDER BY updated_at DESC LIMIT $2",
                tenant_id, limit,
            )
            return [self._row_to_entry(r) for r in rows]

    @staticmethod
    def _row_to_entry(row: Any) -> ProcedureEntry:
        return ProcedureEntry(
            procedure_id=row["procedure_id"],
            tenant_id=row["tenant_id"],
            name=row["name"],
            procedure_type=ProcedureType(row["procedure_type"]),
            description=row["description"],
            steps=tuple(row["steps"]),
            trigger_conditions=tuple(row["trigger_conditions"]),
            tools_required=tuple(row["tools_required"]),
            success_rate=row["success_rate"],
            avg_duration_ms=row["avg_duration_ms"],
            execution_count=row["execution_count"],
            last_executed_at=str(row["last_executed_at"] or ""),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
            tags=tuple(row["tags"]),
        )


class ProceduralMemoryManager:
    """Manages learned procedures and workflows.

    Agents use procedural memory to:
    - Recall proven tool-call sequences
    - Auto-suggest workflows for recognized contexts
    - Track success rates to prefer reliable procedures
    - Learn new procedures from successful multi-step interactions
    """

    def __init__(self, config: ProceduralConfig, backend: ProceduralBackend) -> None:
        self._config = config
        self._backend = backend

    async def register(
        self,
        tenant_id: str,
        name: str,
        procedure_type: ProcedureType,
        steps: list[dict[str, Any]],
        description: str = "",
        trigger_conditions: tuple[str, ...] = (),
        tools_required: tuple[str, ...] = (),
        tags: tuple[str, ...] = (),
    ) -> ProcedureEntry:
        """Register a new procedure."""
        entry = ProcedureEntry(
            tenant_id=tenant_id,
            name=name,
            procedure_type=procedure_type,
            description=description,
            steps=tuple(steps),
            trigger_conditions=trigger_conditions,
            tools_required=tools_required,
            tags=tags,
        )
        await self._backend.upsert(entry)
        logger.info("procedure_registered", name=name, type=procedure_type.value)
        return entry

    async def find_applicable(self, tenant_id: str, context: str) -> list[ProcedureEntry]:
        """Find procedures that match the current context."""
        procedures = await self._backend.find_by_trigger(tenant_id, context)
        return [p for p in procedures if p.success_rate >= self._config.success_rate_threshold]

    async def record_execution(self, procedure_id: str, success: bool, duration_ms: int) -> None:
        """Record the outcome of a procedure execution."""
        await self._backend.update_stats(procedure_id, success, duration_ms)
        logger.debug("procedure_executed", id=procedure_id, success=success)
