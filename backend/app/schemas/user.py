"""User Pydantic schemas — request/response validation."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    model_config = ConfigDict(frozen=True)

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)


class UserUpdate(BaseModel):
    """Schema for updating an existing user (all fields optional)."""

    model_config = ConfigDict(frozen=True)

    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None


class UserResponse(BaseModel):
    """Schema for user data returned to clients."""

    model_config = ConfigDict(frozen=True, from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    created_at: datetime


class UserLogin(BaseModel):
    """Schema for login credentials."""

    model_config = ConfigDict(frozen=True)

    email: EmailStr
    password: str
