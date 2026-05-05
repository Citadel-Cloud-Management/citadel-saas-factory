"""Event Reactor — L4/L5 autonomous event-driven system coordination.

Listens for infrastructure, application, and business events and dispatches
appropriate agent responses based on the current autonomy level.

This is what makes the system self-healing, self-scaling, and self-operating.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

import structlog

from backbone.autonomy.levels import AgenticLevel, check_permission, get_current_level

logger = structlog.get_logger("event_reactor")


class EventCategory(str, Enum):
    """Categories of events the reactor can process."""

    INCIDENT = "incident"              # System failures, degradation
    SCALING = "scaling"                # Load changes, capacity needs
    SECURITY = "security"             # Threats, vulnerabilities
    COMPLIANCE = "compliance"         # Regulatory triggers
    DEPLOYMENT = "deployment"         # Release events
    COST = "cost"                     # Budget alerts
    BUSINESS = "business"             # Revenue, churn, KPIs
    OBSERVABILITY = "observability"   # Metric anomalies


@dataclass(frozen=True)
class SystemEvent:
    """An event from any system that may trigger autonomous action."""

    event_id: str
    category: EventCategory
    severity: str  # critical, high, medium, low
    source: str
    title: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class Reaction:
    """An autonomous action taken in response to an event."""

    event_id: str
    action: str
    agent_domain: str
    agent_type: str
    parameters: dict[str, Any] = field(default_factory=dict)
    requires_approval: bool = False
    approved: bool = False


class EventReactor:
    """Routes system events to appropriate agent reactions.

    At L4+, reactions are executed automatically.
    At L3, reactions are proposed and await human approval.
    At L1-L2, events are logged but no autonomous action is taken.
    """

    def __init__(self) -> None:
        self._handlers: dict[EventCategory, list[Callable]] = {}
        self._reaction_log: list[Reaction] = []

    def register_handler(self, category: EventCategory, handler: Callable) -> None:
        """Register an event handler for a category."""
        if category not in self._handlers:
            self._handlers[category] = []
        self._handlers[category].append(handler)

    async def process_event(self, event: SystemEvent) -> list[Reaction]:
        """Process an event and return proposed/executed reactions."""
        level = get_current_level()

        logger.info(
            "event_received",
            event_id=event.event_id,
            category=event.category,
            severity=event.severity,
            level=level.name,
        )

        # L1-L2: Log only, no autonomous action
        if level <= AgenticLevel.DELEGATION:
            logger.info("event_logged_only", event_id=event.event_id, reason="level_too_low")
            return []

        # Determine reactions
        reactions = self._determine_reactions(event)

        # L3: Propose reactions, require human approval
        if level == AgenticLevel.ORCHESTRATION:
            for reaction in reactions:
                if not check_permission(reaction.action):
                    logger.info("reaction_awaiting_approval", reaction=reaction.action)
            return reactions

        # L4-L5: Execute reactions automatically
        executed = []
        for reaction in reactions:
            if check_permission(reaction.action):
                await self._execute_reaction(reaction)
                executed.append(reaction)
            else:
                logger.warning("reaction_blocked", action=reaction.action, level=level.name)

        return executed

    def _determine_reactions(self, event: SystemEvent) -> list[Reaction]:
        """Map an event to appropriate reactions."""
        reactions: list[Reaction] = []

        if event.category == EventCategory.INCIDENT:
            if event.severity in ("critical", "high"):
                reactions.append(Reaction(
                    event_id=event.event_id,
                    action="auto_remediate",
                    agent_domain="devops",
                    agent_type="incident-responder",
                    parameters={"source": event.source, "details": event.details},
                ))

        elif event.category == EventCategory.SCALING:
            reactions.append(Reaction(
                event_id=event.event_id,
                action="auto_scale",
                agent_domain="devops",
                agent_type="auto-scaler",
                parameters=event.details,
            ))

        elif event.category == EventCategory.SECURITY:
            reactions.append(Reaction(
                event_id=event.event_id,
                action="auto_remediate",
                agent_domain="security",
                agent_type="threat-responder",
                parameters=event.details,
                requires_approval=event.severity != "critical",
            ))

        elif event.category == EventCategory.COMPLIANCE:
            reactions.append(Reaction(
                event_id=event.event_id,
                action="compliance_check",
                agent_domain="legal",
                agent_type="compliance-monitor",
                parameters=event.details,
                requires_approval=True,
            ))

        elif event.category == EventCategory.COST:
            reactions.append(Reaction(
                event_id=event.event_id,
                action="cost_optimize",
                agent_domain="finance",
                agent_type="cost-optimizer",
                parameters=event.details,
            ))

        return reactions

    async def _execute_reaction(self, reaction: Reaction) -> None:
        """Execute an autonomous reaction via the agent backbone."""
        logger.info(
            "reaction_executing",
            event_id=reaction.event_id,
            action=reaction.action,
            agent=f"{reaction.agent_domain}:{reaction.agent_type}",
        )
        self._reaction_log.append(reaction)
        # In production, this dispatches to backbone.orchestrator.router
