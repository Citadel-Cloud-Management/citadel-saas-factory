"""Re-export UserService for backwards compatibility."""

from app.services.user import UserService

__all__ = ["UserService"]
