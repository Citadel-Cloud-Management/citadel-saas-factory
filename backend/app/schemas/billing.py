"""Billing Pydantic schemas — request/response validation for billing endpoints."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.tenant import PlanTier


class CheckoutRequest(BaseModel):
    """Request body for creating a Stripe Checkout session."""

    model_config = ConfigDict(frozen=True)

    plan: PlanTier = Field(description="Target plan tier for upgrade")
    success_url: str = Field(
        min_length=1,
        max_length=2048,
        description="URL to redirect to after successful checkout",
    )
    cancel_url: str = Field(
        min_length=1,
        max_length=2048,
        description="URL to redirect to if checkout is cancelled",
    )


class PortalRequest(BaseModel):
    """Request body for creating a Stripe Customer Portal session."""

    model_config = ConfigDict(frozen=True)

    return_url: str = Field(
        min_length=1,
        max_length=2048,
        description="URL to return to after the portal session",
    )


class SubscriptionResponse(BaseModel):
    """Response schema for current subscription status."""

    model_config = ConfigDict(frozen=True, from_attributes=True)

    plan: PlanTier
    status: str
    current_period_start: datetime | None = None
    current_period_end: datetime | None = None
    stripe_customer_id: str | None = None


class PlanFeatures(BaseModel):
    """Feature limits for a plan tier."""

    model_config = ConfigDict(frozen=True)

    max_users: int
    max_agents: int
    max_storage_gb: int
    api_rate_limit: int
    support: str
    custom_domain: bool
    sso: bool
    audit_log: bool


class PlanResponse(BaseModel):
    """Response schema for a single plan with pricing and features."""

    model_config = ConfigDict(frozen=True)

    name: str
    price_monthly: int
    features: PlanFeatures
