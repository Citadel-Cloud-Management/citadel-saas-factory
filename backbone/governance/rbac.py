"""RBAC — Role-Based Access Control for agents and tools."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import structlog

logger = structlog.get_logger("rbac")


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    APPROVE = "approve"
    ADMIN = "admin"


@dataclass(frozen=True)
class Role:
    """Immutable role definition."""

    name: str
    permissions: frozenset[Permission]
    allowed_domains: frozenset[str] = frozenset()
    allowed_tools: frozenset[str] = frozenset()
    max_autonomy_level: int = 3
    description: str = ""


@dataclass(frozen=True)
class AccessDecision:
    """Immutable access control decision."""

    allowed: bool
    role: str
    resource: str
    action: str
    reason: str = ""


# Default roles for the agent backbone
DEFAULT_ROLES: dict[str, Role] = {
    "observer": Role(
        name="observer",
        permissions=frozenset({Permission.READ}),
        max_autonomy_level=0,
        description="Read-only access, no execution",
    ),
    "worker": Role(
        name="worker",
        permissions=frozenset({Permission.READ, Permission.EXECUTE}),
        max_autonomy_level=2,
        description="Can read and execute low-risk tasks",
    ),
    "operator": Role(
        name="operator",
        permissions=frozenset({Permission.READ, Permission.WRITE, Permission.EXECUTE}),
        max_autonomy_level=3,
        description="Can read, write, and execute with approval gates",
    ),
    "supervisor": Role(
        name="supervisor",
        permissions=frozenset({Permission.READ, Permission.WRITE, Permission.EXECUTE, Permission.APPROVE}),
        max_autonomy_level=4,
        description="Full operational access with approval authority",
    ),
    "admin": Role(
        name="admin",
        permissions=frozenset(Permission),
        max_autonomy_level=5,
        description="Unrestricted access",
    ),
}


class RBACManager:
    """Manages role assignments and access control decisions.

    Enforces:
    - Which agents can access which tools
    - Which domains an agent can operate in
    - Maximum autonomy level per role
    - Approval requirements for high-risk operations
    """

    def __init__(self) -> None:
        self._roles: dict[str, Role] = dict(DEFAULT_ROLES)
        self._assignments: dict[str, str] = {}  # agent_id -> role_name

    def add_role(self, role: Role) -> None:
        self._roles[role.name] = role

    def assign_role(self, agent_id: str, role_name: str) -> None:
        if role_name not in self._roles:
            raise ValueError(f"Role not found: {role_name}")
        self._assignments[agent_id] = role_name
        logger.info("role_assigned", agent_id=agent_id, role=role_name)

    def check_access(
        self,
        agent_id: str,
        resource: str,
        action: Permission,
    ) -> AccessDecision:
        """Check if an agent has permission to perform an action on a resource."""
        role_name = self._assignments.get(agent_id, "observer")
        role = self._roles.get(role_name)

        if not role:
            return AccessDecision(
                allowed=False,
                role=role_name,
                resource=resource,
                action=action.value,
                reason=f"Role not found: {role_name}",
            )

        if action not in role.permissions:
            logger.warning(
                "access_denied",
                agent_id=agent_id,
                role=role_name,
                resource=resource,
                action=action.value,
            )
            return AccessDecision(
                allowed=False,
                role=role_name,
                resource=resource,
                action=action.value,
                reason=f"Permission {action.value} not in role {role_name}",
            )

        if role.allowed_domains and not any(resource.startswith(d) for d in role.allowed_domains):
            return AccessDecision(
                allowed=False,
                role=role_name,
                resource=resource,
                action=action.value,
                reason=f"Domain not allowed for role {role_name}",
            )

        return AccessDecision(
            allowed=True,
            role=role_name,
            resource=resource,
            action=action.value,
        )

    def get_agent_role(self, agent_id: str) -> Role | None:
        role_name = self._assignments.get(agent_id)
        return self._roles.get(role_name) if role_name else None
