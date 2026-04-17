"""Agent Registry — loads agents from _registry.yaml and registers them with the Router."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog
import yaml

from backbone.agents.base import AgentConfig, LLMAgent
from backbone.orchestrator.router import Router

logger = structlog.get_logger("agent_registry")


def load_registry(
    registry_path: str = ".claude/agents/_registry.yaml",
    router: Router | None = None,
) -> Router:
    """Load all agents from the YAML registry and register them with a Router.

    Supports two YAML formats:
    1. Flat list: `agents: [{id, domain, ...}, ...]` (Citadel format)
    2. Nested: `domains: [{name, agents: [...]}, ...]`

    Args:
        registry_path: Path to the agent registry YAML file.
        router: Existing router to add agents to, or creates a new one.

    Returns:
        Router with all agents registered.
    """
    router = router or Router()
    path = Path(registry_path)

    if not path.exists():
        logger.warning("registry_not_found", path=str(path))
        return router

    with open(path) as f:
        registry = yaml.safe_load(f)

    if not registry:
        logger.warning("registry_empty", path=str(path))
        return router

    agent_count = 0

    # Format 1: flat list under "agents" key (Citadel _registry.yaml)
    if "agents" in registry and isinstance(registry["agents"], list):
        for agent_def in registry["agents"]:
            domain = agent_def.get("domain", "unknown")
            agent = _build_agent(domain, agent_def)
            router.register(agent)
            agent_count += 1

    # Format 2: nested domains
    elif "domains" in registry:
        for domain_entry in _iterate_domains(registry["domains"]):
            domain_name = domain_entry.get("name", "unknown")
            agents = domain_entry.get("agents", [])
            for agent_def in agents:
                agent = _build_agent(domain_name, agent_def)
                router.register(agent)
                agent_count += 1

    logger.info("registry_loaded", agent_count=agent_count, path=str(path))
    return router


def _iterate_domains(domains: Any) -> list[dict[str, Any]]:
    """Handle both list and dict domain formats."""
    if isinstance(domains, list):
        return domains
    if isinstance(domains, dict):
        return [
            {"name": k, "agents": v if isinstance(v, list) else v.get("agents", [])}
            for k, v in domains.items()
        ]
    return []


def _build_agent(domain: str, agent_def: dict[str, Any]) -> LLMAgent:
    """Build an LLMAgent from a registry entry."""
    agent_id = agent_def.get("id", agent_def.get("name", "unknown"))
    actual_domain = agent_def.get("domain", domain)
    description = agent_def.get("description", "")
    tools = agent_def.get("tools", [])

    config = AgentConfig(
        name=agent_id,
        domain=actual_domain,
        agent_type=agent_id,
        description=description,
        allowed_tools=tuple(tools) if tools else (),
    )

    system_prompt = (
        f"You are {agent_id}, a specialized {actual_domain} agent.\n"
        f"Role: {description}\n"
        f"Domain: {actual_domain}\n"
        f"Allowed tools: {', '.join(tools) if tools else 'none'}"
    )

    return LLMAgent(
        domain=actual_domain,
        agent_type=agent_id,
        system_prompt=system_prompt,
        config=config,
    )
