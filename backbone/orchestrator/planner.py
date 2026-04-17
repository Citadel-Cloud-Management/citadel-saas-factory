"""Planner — decomposes goals into executable task graphs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import structlog

logger = structlog.get_logger("planner")


class TaskPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class PlanTask:
    """Immutable task within a plan."""

    task_id: str
    name: str
    description: str
    domain: str
    agent_type: str
    priority: TaskPriority = TaskPriority.MEDIUM
    risk_level: RiskLevel = RiskLevel.LOW
    depends_on: tuple[str, ...] = field(default_factory=tuple)
    required_tools: tuple[str, ...] = field(default_factory=tuple)
    estimated_seconds: int = 60
    requires_approval: bool = False
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TaskPlan:
    """Immutable execution plan — a DAG of PlanTasks."""

    plan_id: str
    goal: str
    tasks: tuple[PlanTask, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_execution_batches(self) -> list[list[PlanTask]]:
        """Topological sort tasks into parallel-executable batches.

        Tasks with no unresolved dependencies go into the same batch.
        """
        completed: set[str] = set()
        remaining = list(self.tasks)
        batches: list[list[PlanTask]] = []

        while remaining:
            batch = [
                t for t in remaining
                if all(dep in completed for dep in t.depends_on)
            ]
            if not batch:
                logger.error("circular_dependency", remaining=[t.task_id for t in remaining])
                batch = remaining[:1]

            batches.append(batch)
            completed.update(t.task_id for t in batch)
            remaining = [t for t in remaining if t.task_id not in completed]

        return batches

    def get_critical_path(self) -> list[PlanTask]:
        """Return the longest dependency chain (critical path)."""
        task_map = {t.task_id: t for t in self.tasks}
        memo: dict[str, int] = {}

        def _depth(task_id: str) -> int:
            if task_id in memo:
                return memo[task_id]
            task = task_map.get(task_id)
            if not task or not task.depends_on:
                memo[task_id] = 1
                return 1
            d = 1 + max(_depth(dep) for dep in task.depends_on)
            memo[task_id] = d
            return d

        for t in self.tasks:
            _depth(t.task_id)

        path_tasks = sorted(self.tasks, key=lambda t: memo.get(t.task_id, 0), reverse=True)
        return path_tasks


class Planner:
    """Decomposes a goal into a TaskPlan (DAG of PlanTasks).

    Uses domain registry to understand which agents are available
    and builds dependency graphs for parallel execution.
    """

    def __init__(self, registry_path: str = ".claude/agents/_registry.yaml") -> None:
        self.registry_path = registry_path
        self._domain_map: dict[str, list[str]] = {}

    async def create_plan(
        self,
        goal: str,
        context: dict[str, Any],
    ) -> TaskPlan:
        """Create an execution plan for a goal.

        This is the LLM-assisted planning step. In production, this calls
        an LLM to decompose the goal. Here we provide the structural framework.
        """
        import uuid

        plan_id = f"plan-{uuid.uuid4().hex[:8]}"

        logger.info("planning_start", plan_id=plan_id, goal=goal)

        analysis_task = PlanTask(
            task_id=f"{plan_id}-analyze",
            name="Analyze Goal",
            description=f"Analyze and decompose: {goal}",
            domain="executive",
            agent_type="ceo-strategist",
            priority=TaskPriority.HIGH,
        )

        execution_task = PlanTask(
            task_id=f"{plan_id}-execute",
            name="Execute Primary Work",
            description=f"Execute primary task for: {goal}",
            domain=context.get("domain", "engineering"),
            agent_type=context.get("agent_type", "eng-api-designer"),
            priority=TaskPriority.HIGH,
            depends_on=(analysis_task.task_id,),
        )

        review_task = PlanTask(
            task_id=f"{plan_id}-review",
            name="Review Output",
            description="Review and validate execution output",
            domain="qa-testing",
            agent_type="code-reviewer",
            priority=TaskPriority.MEDIUM,
            depends_on=(execution_task.task_id,),
        )

        return TaskPlan(
            plan_id=plan_id,
            goal=goal,
            tasks=(analysis_task, execution_task, review_task),
            metadata={"context": context},
        )
