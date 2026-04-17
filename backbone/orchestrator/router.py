"""Router — dispatches tasks to the correct specialized agent."""

from __future__ import annotations

from typing import Any

import structlog

from backbone.agents.base import BaseAgent, NoOpAgent
from backbone.orchestrator.planner import PlanTask

logger = structlog.get_logger("router")


class Router:
    """Routes PlanTasks to specialized agents based on domain and type.

    Maintains a registry of available agents and their capabilities.
    Falls back to a NoOp agent if no match is found.
    """

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}
        self._domain_map: dict[str, list[str]] = {}

    def register(self, agent: BaseAgent) -> None:
        """Register an agent for routing."""
        key = f"{agent.domain}:{agent.agent_type}"
        self._agents[key] = agent

        if agent.domain not in self._domain_map:
            self._domain_map[agent.domain] = []
        self._domain_map[agent.domain].append(agent.agent_type)

        logger.debug("agent_registered", key=key, domain=agent.domain)

    def route(self, task: PlanTask) -> BaseAgent:
        """Find the best agent for a task.

        Lookup order:
        1. Exact match: domain:agent_type
        2. Domain fallback: first agent in the domain
        3. NoOp fallback: log warning and return no-op agent
        """
        exact_key = f"{task.domain}:{task.agent_type}"
        agent = self._agents.get(exact_key)
        if agent:
            logger.info("routed_exact", task=task.task_id, agent=exact_key)
            return agent

        domain_agents = self._domain_map.get(task.domain, [])
        if domain_agents:
            fallback_key = f"{task.domain}:{domain_agents[0]}"
            agent = self._agents.get(fallback_key)
            if agent:
                logger.warning(
                    "routed_fallback",
                    task=task.task_id,
                    requested=exact_key,
                    actual=fallback_key,
                )
                return agent

        logger.error("no_agent_found", task=task.task_id, domain=task.domain, type=task.agent_type)
        return NoOpAgent(domain=task.domain, agent_type=task.agent_type)

    def list_agents(self) -> dict[str, list[str]]:
        """Return available agents grouped by domain."""
        return dict(self._domain_map)

    def has_agent(self, domain: str, agent_type: str) -> bool:
        """Check if a specific agent is registered."""
        return f"{domain}:{agent_type}" in self._agents
