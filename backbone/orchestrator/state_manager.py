"""State Manager — tracks execution state, task status, run history."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import structlog

logger = structlog.get_logger("state_manager")


class ExecutionState(str, Enum):
    PENDING = "pending"
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskState:
    """Mutable state for a single task within a run."""

    task_id: str
    status: str = "pending"
    started_at: str | None = None
    completed_at: str | None = None
    output: Any = None
    error: str | None = None
    retries: int = 0


@dataclass
class RunState:
    """Mutable state for an execution run."""

    run_id: str
    goal: str
    state: ExecutionState = ExecutionState.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    plan: Any = None
    tasks: dict[str, TaskState] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class StateManager:
    """Manages execution state across all runs.

    Tracks:
    - Run lifecycle (pending → planning → executing → completed/failed)
    - Task status within each run
    - Retry counts and error history
    - Execution history for audit
    """

    def __init__(self) -> None:
        self._runs: dict[str, RunState] = {}

    def create_run(self, run_id: str, goal: str) -> RunState:
        """Create a new execution run."""
        run = RunState(run_id=run_id, goal=goal)
        self._runs[run_id] = run
        logger.info("run_created", run_id=run_id, goal=goal)
        return run

    def update_run(
        self,
        run_id: str,
        state: ExecutionState | None = None,
        plan: Any = None,
        **metadata: Any,
    ) -> RunState:
        """Update run state."""
        run = self._runs.get(run_id)
        if not run:
            raise KeyError(f"Run {run_id} not found")

        if state is not None:
            run.state = state
        if plan is not None:
            run.plan = plan
        run.metadata.update(metadata)
        run.updated_at = datetime.now(timezone.utc).isoformat()

        logger.info("run_updated", run_id=run_id, state=run.state.value)
        return run

    def update_task(
        self,
        run_id: str,
        task_id: str,
        status: str,
        output: Any = None,
        error: str | None = None,
    ) -> TaskState:
        """Update task state within a run."""
        run = self._runs.get(run_id)
        if not run:
            raise KeyError(f"Run {run_id} not found")

        now = datetime.now(timezone.utc).isoformat()

        if task_id not in run.tasks:
            run.tasks[task_id] = TaskState(task_id=task_id)

        task = run.tasks[task_id]
        task.status = status
        if status == "in_progress" and task.started_at is None:
            task.started_at = now
        if status in ("completed", "failed"):
            task.completed_at = now
        if output is not None:
            task.output = output
        if error is not None:
            task.error = error
            task.retries += 1

        logger.debug("task_updated", run_id=run_id, task_id=task_id, status=status)
        return task

    def get_run(self, run_id: str) -> RunState | None:
        """Get run state by ID."""
        return self._runs.get(run_id)

    def list_runs(self, state: ExecutionState | None = None) -> list[RunState]:
        """List all runs, optionally filtered by state."""
        runs = list(self._runs.values())
        if state is not None:
            runs = [r for r in runs if r.state == state]
        return sorted(runs, key=lambda r: r.created_at, reverse=True)
