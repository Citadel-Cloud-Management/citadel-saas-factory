"""Execution Engine — the main entry point for running the backbone."""

from __future__ import annotations

from typing import Any

import structlog

from backbone.agents.registry import load_registry
from backbone.governance.rbac import RBACManager
from backbone.memory.manager import MemoryManager
from backbone.observability.tracer import Tracer
from backbone.orchestrator.planner import Planner
from backbone.orchestrator.router import Router
from backbone.orchestrator.state_manager import StateManager
from backbone.orchestrator.supervisor import AutonomyLevel, ExecutionResult, Supervisor
from backbone.policies.safety import SafetyConfig, SafetyGovernor
from backbone.tools.registry import ToolRegistry

logger = structlog.get_logger("engine")


class BackboneEngine:
    """Main entry point for the Citadel Agent Backbone.

    Wires together all 10 layers:
    - Orchestrator (supervisor, planner, router, state manager)
    - Agent registry (loaded from _registry.yaml)
    - Workflow engine
    - Memory manager
    - Tool registry
    - Validation layer
    - Observability (tracer)
    - Safety governor
    - RBAC
    - Runtime execution

    Usage:
        engine = BackboneEngine.create()
        result = await engine.run("Analyze competitor pricing")
    """

    def __init__(
        self,
        supervisor: Supervisor,
        memory: MemoryManager,
        tools: ToolRegistry,
        tracer: Tracer,
        safety: SafetyGovernor,
        rbac: RBACManager,
    ) -> None:
        self._supervisor = supervisor
        self._memory = memory
        self._tools = tools
        self._tracer = tracer
        self._safety = safety
        self._rbac = rbac

    @classmethod
    def create(
        cls,
        registry_path: str = ".claude/agents/_registry.yaml",
        autonomy_level: AutonomyLevel = AutonomyLevel.APPROVAL_GATE,
        safety_config: SafetyConfig | None = None,
    ) -> BackboneEngine:
        """Factory method — creates a fully wired BackboneEngine."""
        router = load_registry(registry_path)
        planner = Planner(registry_path)
        state_manager = StateManager()

        supervisor = Supervisor(
            planner=planner,
            router=router,
            state_manager=state_manager,
            autonomy_level=autonomy_level,
        )

        memory = MemoryManager()
        memory.load_long_term()

        tools = ToolRegistry()
        tracer = Tracer()
        safety = SafetyGovernor(safety_config)
        rbac = RBACManager()

        # Wire RBAC into tool registry for access control enforcement
        tools.set_rbac(rbac)

        logger.info(
            "engine_created",
            autonomy=autonomy_level.name,
            agents=len(router.list_agents()),
        )

        return cls(
            supervisor=supervisor,
            memory=memory,
            tools=tools,
            tracer=tracer,
            safety=safety,
            rbac=rbac,
        )

    async def run(
        self,
        goal: str,
        context: dict[str, Any] | None = None,
        approval_callback: Any | None = None,
    ) -> ExecutionResult:
        """Execute a goal through the full backbone pipeline."""
        if self._safety.is_killed:
            logger.critical("engine_killed", goal=goal)
            return ExecutionResult(
                run_id="killed",
                goal=goal,
                status="killed",
                errors=("Kill switch is active",),
            )

        span = self._tracer.start_trace(operation="backbone.run", service="engine")
        span.tag("goal", goal[:200])

        try:
            # Pre-execution budget check
            budget_check = self._safety.check_budget("pre_check")
            if not budget_check["allowed"]:
                return ExecutionResult(
                    run_id="budget_exceeded",
                    goal=goal,
                    status="budget_exceeded",
                    errors=(budget_check["reason"],),
                )

            result = await self._supervisor.execute(
                goal=goal,
                context=context,
                approval_callback=approval_callback,
            )

            self._safety.record_usage(
                run_id=result.run_id,
                tool_calls=result.completed_steps,
            )

            span.tag("status", result.status)
            span.tag("steps", str(result.total_steps))

            if result.errors:
                span.error("; ".join(result.errors[:3]))

            return result

        except Exception as exc:
            span.error(str(exc))
            raise

        finally:
            self._tracer.record(span.finish())

    async def health(self) -> dict[str, Any]:
        """Return backbone health status."""
        return {
            "status": "killed" if self._safety.is_killed else "healthy",
            "agents": self._supervisor.router.list_agents(),
            "memory_working": len(self._memory._working),
            "memory_long_term": len(self._memory._long_term),
            "tools": len(self._tools.list_tools()),
            "trace_metrics": self._tracer.get_metrics(),
        }
