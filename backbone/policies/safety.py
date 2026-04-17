"""Safety Policies — kill switch, budget governor, confidence gates."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

import structlog

logger = structlog.get_logger("safety")


@dataclass(frozen=True)
class SafetyConfig:
    """Immutable safety configuration."""

    max_tokens_per_run: int = 500_000
    max_tool_calls_per_run: int = 100
    max_cost_usd_per_run: float = 10.0
    min_confidence_threshold: float = 0.7
    kill_switch_enabled: bool = True
    sandbox_mode: bool = False
    require_dual_approval_above_risk: str = "high"


@dataclass
class RunBudget:
    """Mutable budget tracker for a single execution run."""

    tokens_used: int = 0
    tool_calls: int = 0
    cost_usd: float = 0.0
    started_at: float = field(default_factory=time.time)


class SafetyGovernor:
    """Enforces safety policies and budget limits on agent execution.

    Provides:
    - Token budget enforcement
    - Tool call rate limiting
    - Cost ceiling
    - Confidence gating
    - Kill switch (immediate halt)
    - Sandbox mode (dry-run, no side effects)
    """

    def __init__(self, config: SafetyConfig | None = None) -> None:
        self._config = config or SafetyConfig()
        self._budgets: dict[str, RunBudget] = {}
        self._killed = False
        self._killed_by: str = ""
        self._kill_reason: str = ""

    @property
    def is_killed(self) -> bool:
        return self._killed

    def kill(self, reason: str, caller_id: str = "system") -> None:
        """Activate kill switch — halt all execution immediately."""
        self._killed = True
        self._killed_by = caller_id
        self._kill_reason = reason
        logger.critical("kill_switch_activated", reason=reason, caller=caller_id)

    def resume(self, caller_id: str = "", rbac_manager: Any = None) -> None:
        """Deactivate kill switch. Requires admin role via RBAC.

        Fails closed: if no RBAC manager is provided or caller lacks
        APPROVE permission, the kill switch stays active.
        """
        if rbac_manager is None:
            logger.critical("kill_switch_resume_denied", reason="No RBAC manager provided")
            raise PermissionError("Cannot resume kill switch without RBAC verification")

        from backbone.governance.rbac import Permission
        decision = rbac_manager.check_access(caller_id, "safety:kill_switch", Permission.APPROVE)
        if not decision.allowed:
            logger.critical(
                "kill_switch_resume_denied",
                caller=caller_id,
                reason=decision.reason,
            )
            raise PermissionError(f"Caller {caller_id} lacks APPROVE permission to resume kill switch")

        self._killed = False
        logger.critical("kill_switch_deactivated", caller=caller_id)

    def check_budget(self, run_id: str) -> dict[str, Any]:
        """Check if a run is within budget limits."""
        if self._killed:
            return {"allowed": False, "reason": "Kill switch active"}

        budget = self._budgets.get(run_id)
        if not budget:
            budget = RunBudget()
            self._budgets[run_id] = budget

        violations: list[str] = []

        if budget.tokens_used >= self._config.max_tokens_per_run:
            violations.append(f"Token limit exceeded: {budget.tokens_used}/{self._config.max_tokens_per_run}")

        if budget.tool_calls >= self._config.max_tool_calls_per_run:
            violations.append(f"Tool call limit exceeded: {budget.tool_calls}/{self._config.max_tool_calls_per_run}")

        if budget.cost_usd >= self._config.max_cost_usd_per_run:
            violations.append(f"Cost limit exceeded: ${budget.cost_usd:.2f}/${self._config.max_cost_usd_per_run:.2f}")

        if violations:
            logger.warning("budget_violation", run_id=run_id, violations=violations)
            return {"allowed": False, "reason": "; ".join(violations)}

        return {"allowed": True, "budget": {
            "tokens_remaining": self._config.max_tokens_per_run - budget.tokens_used,
            "tool_calls_remaining": self._config.max_tool_calls_per_run - budget.tool_calls,
            "cost_remaining_usd": self._config.max_cost_usd_per_run - budget.cost_usd,
        }}

    def record_usage(
        self,
        run_id: str,
        tokens: int = 0,
        tool_calls: int = 0,
        cost_usd: float = 0.0,
    ) -> None:
        """Record resource usage for a run."""
        if run_id not in self._budgets:
            self._budgets[run_id] = RunBudget()

        budget = self._budgets[run_id]
        budget.tokens_used += tokens
        budget.tool_calls += tool_calls
        budget.cost_usd += cost_usd

    def check_confidence(self, score: float) -> bool:
        """Check if confidence score meets minimum threshold."""
        return score >= self._config.min_confidence_threshold
