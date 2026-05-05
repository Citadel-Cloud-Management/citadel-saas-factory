"""Self-Healing Engine — L4/L5 autonomous remediation.

Monitors system health and automatically remediates common failure patterns:
- Pod crash loops → restart with increased resources
- Database connection exhaustion → scale connection pool
- High error rates → rollback deployment
- Certificate expiry → auto-rotate
- Disk pressure → clean up and expand volumes
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import structlog

from backbone.autonomy.levels import check_permission

logger = structlog.get_logger("self_healing")


class RemediationType(str, Enum):
    RESTART_POD = "restart_pod"
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    ROLLBACK = "rollback"
    ROTATE_SECRET = "rotate_secret"
    CLEAR_CACHE = "clear_cache"
    EXPAND_STORAGE = "expand_storage"
    FAILOVER_DB = "failover_db"
    BLOCK_IP = "block_ip"
    RATE_LIMIT = "rate_limit"


@dataclass(frozen=True)
class RemediationAction:
    """A specific remediation to execute."""

    remediation_type: RemediationType
    target: str
    parameters: dict[str, Any]
    risk_level: str  # low, medium, high
    rollback_possible: bool = True


class SelfHealingEngine:
    """Detects failure patterns and executes remediation playbooks.

    Only operates at L4+ autonomy. At L3, proposes actions for human review.
    """

    def __init__(self) -> None:
        self._playbooks: dict[str, list[RemediationAction]] = {}
        self._register_default_playbooks()

    def _register_default_playbooks(self) -> None:
        """Register standard remediation playbooks."""
        self._playbooks["high_error_rate"] = [
            RemediationAction(
                remediation_type=RemediationType.ROLLBACK,
                target="deployment/citadel-backend",
                parameters={"revision": "previous"},
                risk_level="medium",
            ),
        ]
        self._playbooks["pod_crash_loop"] = [
            RemediationAction(
                remediation_type=RemediationType.RESTART_POD,
                target="deployment/citadel-backend",
                parameters={"increase_memory": True, "factor": 1.5},
                risk_level="low",
            ),
        ]
        self._playbooks["high_latency"] = [
            RemediationAction(
                remediation_type=RemediationType.SCALE_UP,
                target="deployment/citadel-backend",
                parameters={"replicas_delta": 2},
                risk_level="low",
            ),
            RemediationAction(
                remediation_type=RemediationType.CLEAR_CACHE,
                target="redis/citadel",
                parameters={"pattern": "cache:*"},
                risk_level="low",
            ),
        ]
        self._playbooks["db_connection_exhaustion"] = [
            RemediationAction(
                remediation_type=RemediationType.SCALE_UP,
                target="rds/citadel-production",
                parameters={"max_capacity_delta": 4},
                risk_level="medium",
            ),
        ]
        self._playbooks["security_threat"] = [
            RemediationAction(
                remediation_type=RemediationType.BLOCK_IP,
                target="waf/citadel",
                parameters={},
                risk_level="low",
            ),
            RemediationAction(
                remediation_type=RemediationType.RATE_LIMIT,
                target="alb/citadel",
                parameters={"requests_per_second": 10},
                risk_level="low",
            ),
        ]

    async def diagnose_and_heal(self, symptom: str, context: dict[str, Any]) -> list[RemediationAction]:
        """Diagnose a system issue and execute appropriate remediation.

        Args:
            symptom: The observed failure pattern (key into playbooks).
            context: Additional context about the failure.

        Returns:
            List of remediation actions taken or proposed.
        """
        playbook = self._playbooks.get(symptom, [])
        if not playbook:
            logger.warning("no_playbook", symptom=symptom)
            return []

        executed: list[RemediationAction] = []
        for action in playbook:
            if check_permission("auto_remediate"):
                logger.info(
                    "executing_remediation",
                    type=action.remediation_type,
                    target=action.target,
                    risk=action.risk_level,
                )
                await self._execute(action, context)
                executed.append(action)
            else:
                logger.info(
                    "remediation_proposed",
                    type=action.remediation_type,
                    target=action.target,
                    awaiting="human_approval",
                )
                executed.append(action)

        return executed

    async def _execute(self, action: RemediationAction, context: dict[str, Any]) -> None:
        """Execute a single remediation action against the target system."""
        # In production: dispatch to K8s API, AWS SDK, or agent backbone
        logger.info(
            "remediation_executed",
            type=action.remediation_type.value,
            target=action.target,
            params=action.parameters,
        )
