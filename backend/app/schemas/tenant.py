"""Tenant Pydantic schemas — request/response validation."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.tenant import PlanTier


class TenantCreate(BaseModel):
    """Schema for creating a new tenant."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=63, pattern=r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")
    plan: PlanTier = PlanTier.FREE


class TenantUpdate(BaseModel):
    """Schema for updating an existing tenant (all fields optional)."""

    model_config = ConfigDict(frozen=True)

    name: str | None = Field(default=None, min_length=1, max_length=255)
    plan: PlanTier | None = None


class TenantResponse(BaseModel):
    """Schema for tenant data returned to clients."""

    model_config = ConfigDict(frozen=True, from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    plan: PlanTier
    is_active: bool
    created_at: datetime
