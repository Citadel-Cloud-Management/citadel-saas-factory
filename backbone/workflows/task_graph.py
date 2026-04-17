"""Task Graph — DAG-based workflow execution engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Coroutine

import structlog

logger = structlog.get_logger("task_graph")


class FlowPattern(str, Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    EVENT_DRIVEN = "event_driven"
    HUMAN_IN_LOOP = "human_in_loop"


@dataclass(frozen=True)
class GraphNode:
    """Immutable node in a task graph."""

    node_id: str
    name: str
    handler: str
    depends_on: tuple[str, ...] = field(default_factory=tuple)
    pattern: FlowPattern = FlowPattern.SEQUENTIAL
    approval_required: bool = False
    timeout_seconds: int = 300
    retry_policy: dict[str, Any] = field(default_factory=lambda: {"max_retries": 3, "backoff": "exponential"})


@dataclass(frozen=True)
class TaskGraph:
    """Immutable DAG of GraphNodes representing a workflow."""

    graph_id: str
    name: str
    nodes: tuple[GraphNode, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_root_nodes(self) -> list[GraphNode]:
        """Nodes with no dependencies — workflow entry points."""
        return [n for n in self.nodes if not n.depends_on]

    def get_dependents(self, node_id: str) -> list[GraphNode]:
        """Nodes that depend on the given node."""
        return [n for n in self.nodes if node_id in n.depends_on]

    def validate(self) -> list[str]:
        """Validate graph structure: no cycles, no missing deps."""
        errors: list[str] = []
        node_ids = {n.node_id for n in self.nodes}

        for node in self.nodes:
            for dep in node.depends_on:
                if dep not in node_ids:
                    errors.append(f"Node {node.node_id} depends on missing node {dep}")

        visited: set[str] = set()
        path: set[str] = set()

        def _has_cycle(nid: str) -> bool:
            if nid in path:
                return True
            if nid in visited:
                return False
            visited.add(nid)
            path.add(nid)
            for dep_node in self.get_dependents(nid):
                if _has_cycle(dep_node.node_id):
                    return True
            path.discard(nid)
            return False

        for node in self.nodes:
            if _has_cycle(node.node_id):
                errors.append(f"Cycle detected involving node {node.node_id}")
                break

        return errors


class WorkflowEngine:
    """Executes TaskGraphs respecting dependencies, patterns, and approval gates."""

    def __init__(self) -> None:
        self._handlers: dict[str, Callable[..., Coroutine]] = {}
        self._approval_callback: Callable | None = None

    def register_handler(self, name: str, handler: Callable[..., Coroutine]) -> None:
        self._handlers[name] = handler

    def set_approval_callback(self, callback: Callable) -> None:
        self._approval_callback = callback

    async def execute(self, graph: TaskGraph, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a task graph end-to-end."""
        errors = graph.validate()
        if errors:
            return {"status": "invalid", "errors": errors}

        ctx = dict(context or {})
        results: dict[str, Any] = {}
        completed: set[str] = set()

        remaining = list(graph.nodes)
        while remaining:
            batch = [
                n for n in remaining
                if all(d in completed for d in n.depends_on)
            ]
            if not batch:
                return {"status": "deadlock", "completed": list(completed)}

            for node in batch:
                if node.approval_required and self._approval_callback:
                    approved = await self._approval_callback(node)
                    if not approved:
                        return {"status": "approval_denied", "node": node.node_id}

                handler = self._handlers.get(node.handler)
                if handler:
                    try:
                        result = await handler(node, ctx)
                        results[node.node_id] = result
                        ctx[node.node_id] = result
                    except Exception as exc:
                        logger.error("node_failed", node=node.node_id, error=str(exc))
                        results[node.node_id] = {"error": str(exc)}
                else:
                    logger.warning("handler_not_found", node=node.node_id, handler=node.handler)

                completed.add(node.node_id)

            remaining = [n for n in remaining if n.node_id not in completed]

        return {"status": "completed", "results": results}
