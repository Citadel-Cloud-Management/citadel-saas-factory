"""Role-based access control — permissions, role mappings, and FastAPI dependencies."""

from enum import Enum
from typing import Any

from fastapi import HTTPException, Request, status

from app.api.deps import get_current_user


class Permission(str, Enum):
    """Fine-grained permissions for route-level RBAC."""

    USERS_READ = "users:read"
    USERS_WRITE = "users:write"
    USERS_DELETE = "users:delete"
    TENANTS_READ = "tenants:read"
    TENANTS_WRITE = "tenants:write"
    TENANTS_DELETE = "tenants:delete"
    AGENTS_READ = "agents:read"
    AGENTS_WRITE = "agents:write"
    SETTINGS_READ = "settings:read"
    SETTINGS_WRITE = "settings:write"
    BILLING_READ = "billing:read"
    BILLING_WRITE = "billing:write"
    ADMIN = "admin"


_VIEWER_PERMISSIONS: frozenset[Permission] = frozenset({
    Permission.USERS_READ,
    Permission.AGENTS_READ,
    Permission.SETTINGS_READ,
})

_MEMBER_PERMISSIONS: frozenset[Permission] = _VIEWER_PERMISSIONS | frozenset({
    Permission.USERS_WRITE,
    Permission.SETTINGS_WRITE,
})

_ADMIN_PERMISSIONS: frozenset[Permission] = _MEMBER_PERMISSIONS | frozenset({
    Permission.USERS_DELETE,
    Permission.TENANTS_READ,
    Permission.TENANTS_WRITE,
    Permission.BILLING_READ,
    Permission.BILLING_WRITE,
})

_OWNER_PERMISSIONS: frozenset[Permission] = _ADMIN_PERMISSIONS | frozenset({
    Permission.TENANTS_DELETE,
    Permission.AGENTS_WRITE,
    Permission.ADMIN,
})

_SUPERUSER_PERMISSIONS: frozenset[Permission] = frozenset(Permission)

ROLE_PERMISSIONS: dict[str, frozenset[Permission]] = {
    "viewer": _VIEWER_PERMISSIONS,
    "member": _MEMBER_PERMISSIONS,
    "admin": _ADMIN_PERMISSIONS,
    "owner": _OWNER_PERMISSIONS,
    "superuser": _SUPERUSER_PERMISSIONS,
}


def _get_permissions_for_role(role: str) -> frozenset[Permission]:
    """Return the permission set for a given role name.

    Falls back to an empty set for unknown roles so that unrecognised
    roles are deny-by-default.
    """
    return ROLE_PERMISSIONS.get(role, frozenset())


def require_permission(*perms: Permission):
    """Return a FastAPI dependency that enforces the listed permissions.

    Usage::

        @router.get("/users", dependencies=[Depends(require_permission(Permission.USERS_READ))])
        async def list_users(...): ...

    The dependency extracts the ``role`` claim from the JWT payload
    (populated by ``get_current_user``) and verifies that the role
    grants every requested permission.  Raises 403 otherwise.
    """

    async def _check(request: Request) -> dict[str, Any]:
        user = await get_current_user(request)
        role: str = user.get("role", "member")
        granted = _get_permissions_for_role(role)

        missing = {p for p in perms if p not in granted}
        if missing:
            missing_labels = ", ".join(sorted(m.value for m in missing))
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {missing_labels}",
            )
        return user

    return _check
