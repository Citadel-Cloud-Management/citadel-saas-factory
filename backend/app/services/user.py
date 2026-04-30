"""User service — business logic for user management."""

import uuid

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(plain: str) -> str:
    """Hash a plaintext password with bcrypt."""
    return pwd_context.hash(plain)


def _verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return pwd_context.verify(plain, hashed)


class UserService:
    """Orchestrates user-related business logic."""

    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserRepository(session)

    async def create_user(
        self,
        data: UserCreate,
        tenant_id: uuid.UUID,
    ) -> User:
        """Create a new user with a hashed password."""
        existing = await self._repo.get_by_email(data.email)
        if existing is not None:
            msg = f"User with email {data.email} already exists"
            raise ValueError(msg)

        return await self._repo.create(
            email=data.email,
            hashed_password=_hash_password(data.password),
            full_name=data.full_name,
            tenant_id=tenant_id,
        )

    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> User | None:
        """Verify credentials and return the user, or None on failure."""
        user = await self._repo.get_by_email(email)
        if user is None:
            return None
        if not _verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    async def get_user(
        self,
        user_id: uuid.UUID,
        tenant_id: uuid.UUID | None = None,
    ) -> User | None:
        """Fetch a single user by ID."""
        return await self._repo.get_by_id(user_id, tenant_id)

    async def update_user(
        self,
        user_id: uuid.UUID,
        data: UserUpdate,
        tenant_id: uuid.UUID | None = None,
    ) -> User | None:
        """Update user fields. Returns None if not found."""
        update_fields = data.model_dump(exclude_unset=True)
        if not update_fields:
            return await self._repo.get_by_id(user_id, tenant_id)
        return await self._repo.update(user_id, tenant_id, **update_fields)

    async def list_users(
        self,
        tenant_id: uuid.UUID | None = None,
        *,
        page: int = 1,
        limit: int = 20,
    ) -> tuple[list[User], int]:
        """List users with pagination."""
        return await self._repo.get_all(tenant_id=tenant_id, page=page, limit=limit)
