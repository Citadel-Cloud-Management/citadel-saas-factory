"""Agent registry endpoints — read-only access to the agent catalog."""

import os
from collections import defaultdict
from functools import lru_cache
from typing import Any

import yaml
from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter(prefix="/agents", tags=["agents"])

_REGISTRY_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "..", ".claude", "agents", "_registry.yaml",
)


@lru_cache(maxsize=1)
def _load_registry() -> list[dict[str, Any]]:
    """Load and cache the agent registry from YAML.

    Returns an empty list if the file is missing or malformed.
    """
    path = os.path.normpath(_REGISTRY_PATH)
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        return []
    agents: list[dict[str, Any]] = data.get("agents", [])
    return agents if isinstance(agents, list) else []


def _envelope(
    data: Any,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Wrap a response in the standard envelope."""
    return {"data": data, "error": None, "meta": meta or {}}


@router.get("/domains", status_code=status.HTTP_200_OK)
async def list_domains() -> dict[str, Any]:
    """List all available agent domains with agent counts."""
    agents = _load_registry()
    counts: dict[str, int] = defaultdict(int)
    for agent in agents:
        domain = agent.get("domain", "unknown")
        counts[domain] += 1
    domain_list = [
        {"domain": d, "agent_count": c}
        for d, c in sorted(counts.items())
    ]
    return _envelope(data=domain_list, meta={"total": len(domain_list)})


@router.get("/", status_code=status.HTTP_200_OK)
async def list_agents(
    domain: str | None = Query(None, description="Filter by domain"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
) -> dict[str, Any]:
    """List all agents from the registry (paginated, filterable by domain)."""
    agents = _load_registry()
    if domain:
        agents = [a for a in agents if a.get("domain") == domain]

    total = len(agents)
    start = (page - 1) * limit
    page_items = agents[start : start + limit]

    return _envelope(
        data=page_items,
        meta={"total": total, "page": page, "limit": limit},
    )


@router.get("/{agent_id}", status_code=status.HTTP_200_OK)
async def get_agent(agent_id: str) -> dict[str, Any]:
    """Get a single agent's details by ID."""
    agents = _load_registry()
    for agent in agents:
        if agent.get("id") == agent_id:
            return _envelope(data=agent)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Agent '{agent_id}' not found",
    )
