"""Auth package — role-based access control primitives."""

from app.auth.permissions import ROLE_PERMISSIONS, Permission, require_permission

__all__ = [
    "Permission",
    "ROLE_PERMISSIONS",
    "require_permission",
]
