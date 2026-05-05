"""Agentic Engineering Levels — Progressive autonomy from L1 to L5.

L1 — Interactive Expertise: AI responds to humans (ChatGPT mode)
L2 — Delegation: Humans assign tasks to AI agents
L3 — Human Orchestration: Humans coordinate multiple specialized agents
L4 — System Orchestration: Systems autonomously coordinate other systems
L5 — Full Autonomy: AI systems operate entire workflows end-to-end
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

import structlog

logger = structlog.get_logger("autonomy")


class AgenticLevel(IntEnum):
    """The 5 levels of agentic engineering."""

    INTERACTIVE = 1      # L1: AI responds to humans
    DELEGATION = 2       # L2: Humans assign tasks to agents
    ORCHESTRATION = 3    # L3: Humans coordinate multiple agents
    SYSTEM_ORCH = 4      # L4: Systems coordinate systems autonomously
    FULL_AUTONOMY = 5    # L5: AI operates entire workflows end-to-end


@dataclass(frozen=True)
class AutonomyPolicy:
    """Defines what actions are permitted at each autonomy level."""

    level: AgenticLevel
    can_deploy: bool = False
    can_auto_remediate: bool = False
    can_auto_scale: bool = False
    can_manage_secrets: bool = False
    can_approve_spend: bool = False
    can_merge_code: bool = False
    can_modify_infra: bool = False
    requires_human_approval: tuple[str, ...] = field(default_factory=tuple)
    max_concurrent_agents: int = 1
    budget_limit_usd: float = 0.0


# Policy matrix — what each level is allowed to do
LEVEL_POLICIES: dict[AgenticLevel, AutonomyPolicy] = {
    AgenticLevel.INTERACTIVE: AutonomyPolicy(
        level=AgenticLevel.INTERACTIVE,
        max_concurrent_agents=1,
        requires_human_approval=("all",),
    ),
    AgenticLevel.DELEGATION: AutonomyPolicy(
        level=AgenticLevel.DELEGATION,
        max_concurrent_agents=5,
        can_auto_remediate=False,
        requires_human_approval=("deploy", "infra", "secrets", "spend"),
        budget_limit_usd=10.0,
    ),
    AgenticLevel.ORCHESTRATION: AutonomyPolicy(
        level=AgenticLevel.ORCHESTRATION,
        max_concurrent_agents=30,
        can_auto_remediate=True,
        can_auto_scale=True,
        requires_human_approval=("deploy_production", "secrets", "spend_over_50"),
        budget_limit_usd=50.0,
    ),
    AgenticLevel.SYSTEM_ORCH: AutonomyPolicy(
        level=AgenticLevel.SYSTEM_ORCH,
        can_deploy=True,
        can_auto_remediate=True,
        can_auto_scale=True,
        can_modify_infra=True,
        max_concurrent_agents=100,
        requires_human_approval=("production_deploy", "secret_rotation", "budget_increase"),
        budget_limit_usd=200.0,
    ),
    AgenticLevel.FULL_AUTONOMY: AutonomyPolicy(
        level=AgenticLevel.FULL_AUTONOMY,
        can_deploy=True,
        can_auto_remediate=True,
        can_auto_scale=True,
        can_manage_secrets=True,
        can_approve_spend=True,
        can_merge_code=True,
        can_modify_infra=True,
        max_concurrent_agents=500,
        requires_human_approval=("budget_over_1000", "data_deletion", "compliance_override"),
        budget_limit_usd=1000.0,
    ),
}


def get_current_level() -> AgenticLevel:
    """Read the current autonomy level from environment."""
    level_str = os.environ.get("AGENTIC_LEVEL", "L3")
    level_map = {
        "L1": AgenticLevel.INTERACTIVE,
        "L2": AgenticLevel.DELEGATION,
        "L3": AgenticLevel.ORCHESTRATION,
        "L4": AgenticLevel.SYSTEM_ORCH,
        "L5": AgenticLevel.FULL_AUTONOMY,
    }
    return level_map.get(level_str, AgenticLevel.ORCHESTRATION)


def get_policy() -> AutonomyPolicy:
    """Get the autonomy policy for the current level."""
    return LEVEL_POLICIES[get_current_level()]


def check_permission(action: str) -> bool:
    """Check if an action is permitted at the current autonomy level.

    Args:
        action: The action to check (e.g., 'deploy', 'auto_scale', 'manage_secrets')

    Returns:
        True if permitted, False if requires human approval.
    """
    policy = get_policy()

    if "all" in policy.requires_human_approval:
        return False

    if action in policy.requires_human_approval:
        logger.info("permission_denied", action=action, level=policy.level.name, reason="requires_human_approval")
        return False

    permission_map: dict[str, bool] = {
        "deploy": policy.can_deploy,
        "deploy_production": policy.can_deploy,
        "auto_remediate": policy.can_auto_remediate,
        "auto_scale": policy.can_auto_scale,
        "manage_secrets": policy.can_manage_secrets,
        "approve_spend": policy.can_approve_spend,
        "merge_code": policy.can_merge_code,
        "modify_infra": policy.can_modify_infra,
    }

    permitted = permission_map.get(action, False)
    logger.info("permission_check", action=action, level=policy.level.name, permitted=permitted)
    return permitted
