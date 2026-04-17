"""Citadel Autonomous Agent Backbone.

A 10-layer architecture for autonomous agent orchestration:

1. Control Layer     — Orchestrator, Planner, Router, State Manager
2. Agent Layer       — Executive, Domain, Utility, Reviewer agents
3. Workflow Layer    — Task graphs, event flows, approval gates
4. Memory Layer      — Working, session, long-term, vector, audit memory
5. Tool Layer        — Internal/external tool registry with auth + rate limits
6. Data Layer        — Schema registry, knowledge connectors, config
7. Validation Layer  — Input/output validation, safety, guardrails
8. Observability     — Traces, logs, metrics, drift detection
9. Runtime Layer     — Queue, scheduler, workers, execution engine
10. Governance Layer — RBAC, audit, compliance, versioning

Usage:
    from backbone import Backbone

    backbone = Backbone.from_config("backbone/config.yaml")
    result = await backbone.execute("Analyze competitor pricing")
"""

from backbone.orchestrator.supervisor import Supervisor
from backbone.orchestrator.planner import Planner
from backbone.orchestrator.router import Router
from backbone.orchestrator.state_manager import StateManager

__all__ = [
    "Supervisor",
    "Planner",
    "Router",
    "StateManager",
]
