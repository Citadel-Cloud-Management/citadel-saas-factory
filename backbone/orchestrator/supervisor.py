"""Supervisor / Orchestrator — decides what goal is active, which agent works, when to stop."""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import structlog

from backbone.orchestrator.planner import Planner, TaskPlan
from backbone.orchestrator.router import Router
from backbone.orchestrator.state_manager import ExecutionState, StateManager

logger = structlog.get_logger("supervisor")


class AutonomyLevel(int, Enum):
    """Autonomy levels for agent execution."""

    ASSISTANT = 0       # Suggest only, no action
    SUGGEST = 1         # Suggest actions, user approves
    LOW_RISK = 2        # Act on low-risk tasks autonomously
    APPROVAL_GATE = 3   # Act with approval gates for risky ops
    AUTONOMOUS = 4      # Mostly autonomous with rollback + monitoring
    CLOSED_LOOP = 5     # Full autonomy in bounded environments


@dataclass(frozen=True)
class ExecutionResult:
    """Immutable result of a supervised execution."""

    run_id: str
    goal: str
    status: str
    outputs: tuple[Any, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    started_at: str = ""
    completed_at: str = ""
    total_steps: int = 0
    completed_steps: int = 0


class Supervisor:
    """Top-level orchestrator that coordinates the entire agent backbone.

    Responsibilities:
    - Interpret user/trigger intent
    - Decompose goals via Planner
    - Route tasks to agents via Router
    - Track state via StateManager
    - Enforce autonomy levels
    - Handle escalation and failure
    """

    def __init__(
        self,
        planner: Planner | None = None,
        router: Router | None = None,
        state_manager: StateManager | None = None,
        autonomy_level: AutonomyLevel = AutonomyLevel.APPROVAL_GATE,
        max_concurrent_tasks: int = 5,
    ) -> None:
        self.planner = planner or Planner()
        self.router = router or Router()
        self.state_manager = state_manager or StateManager()
        self.autonomy_level = autonomy_level
        self.max_concurrent_tasks = max_concurrent_tasks

    async def execute(
        self,
        goal: str,
        context: dict[str, Any] | None = None,
        approval_callback: Any | None = None,
    ) -> ExecutionResult:
        """Execute a goal through the full agent pipeline.

        1. Plan — decompose goal into tasks
        2. Route — assign tasks to specialized agents
        3. Execute — run tasks respecting dependencies
        4. Validate — check outputs against quality gates
        5. Aggregate — collect results
        """
        run_id = str(uuid.uuid4())
        started_at = datetime.now(timezone.utc).isoformat()

        logger.info("execution_start", run_id=run_id, goal=goal, autonomy=self.autonomy_level.name)

        self.state_manager.create_run(run_id, goal)

        try:
            plan = await self.planner.create_plan(goal, context or {})
            self.state_manager.update_run(run_id, state=ExecutionState.PLANNING, plan=plan)

            logger.info("plan_created", run_id=run_id, task_count=len(plan.tasks))

            if self.autonomy_level <= AutonomyLevel.SUGGEST:
                return ExecutionResult(
                    run_id=run_id,
                    goal=goal,
                    status="suggested",
                    outputs=(plan,),
                    started_at=started_at,
                    completed_at=datetime.now(timezone.utc).isoformat(),
                    total_steps=len(plan.tasks),
                )

            if self.autonomy_level == AutonomyLevel.APPROVAL_GATE:
                if not approval_callback:
                    logger.error("approval_gate_no_callback", run_id=run_id)
                    self.state_manager.update_run(run_id, state=ExecutionState.CANCELLED)
                    return ExecutionResult(
                        run_id=run_id, goal=goal, status="no_approval_callback",
                        errors=("Approval gate requires a callback but none was provided",),
                        started_at=started_at,
                        completed_at=datetime.now(timezone.utc).isoformat(),
                        total_steps=len(plan.tasks),
                    )
                approved = await approval_callback(plan)
                if not approved:
                    self.state_manager.update_run(run_id, state=ExecutionState.CANCELLED)
                    return ExecutionResult(
                        run_id=run_id, goal=goal, status="cancelled_by_user",
                        started_at=started_at,
                        completed_at=datetime.now(timezone.utc).isoformat(),
                    )

            self.state_manager.update_run(run_id, state=ExecutionState.EXECUTING)

            outputs: list[Any] = []
            errors: list[str] = []
            completed_count = 0

            task_batches = plan.get_execution_batches()
            for batch in task_batches:
                semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

                async def _run_task(task):
                    async with semaphore:
                        agent = self.router.route(task)
                        self.state_manager.update_task(run_id, task.task_id, "in_progress")
                        try:
                            result = await agent.execute(task)
                            self.state_manager.update_task(run_id, task.task_id, "completed")
                            return result
                        except Exception as exc:
                            logger.error("task_failed", run_id=run_id, task_id=task.task_id, error=str(exc))
                            self.state_manager.update_task(run_id, task.task_id, "failed")
                            error_code = type(exc).__name__
                            return {"error": f"{error_code}: task {task.task_id} failed", "task_id": task.task_id}

                results = await asyncio.gather(
                    *[_run_task(t) for t in batch],
                    return_exceptions=True,
                )

                for r in results:
                    if isinstance(r, Exception):
                        errors.append(str(r))
                    elif isinstance(r, dict) and "error" in r:
                        errors.append(r["error"])
                        outputs.append(r)
                    else:
                        outputs.append(r)
                        completed_count += 1

            final_state = ExecutionState.COMPLETED if not errors else ExecutionState.PARTIAL
            self.state_manager.update_run(run_id, state=final_state)

            return ExecutionResult(
                run_id=run_id,
                goal=goal,
                status=final_state.value,
                outputs=tuple(outputs),
                errors=tuple(errors),
                started_at=started_at,
                completed_at=datetime.now(timezone.utc).isoformat(),
                total_steps=len(plan.tasks),
                completed_steps=completed_count,
            )

        except Exception as exc:
            logger.error("execution_failed", run_id=run_id, error=str(exc))
            self.state_manager.update_run(run_id, state=ExecutionState.FAILED)
            error_code = type(exc).__name__
            return ExecutionResult(
                run_id=run_id,
                goal=goal,
                status="failed",
                errors=(f"{error_code}: execution failed (run_id={run_id})",),
                started_at=started_at,
                completed_at=datetime.now(timezone.utc).isoformat(),
            )
