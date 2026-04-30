"""Billing API endpoints — Stripe checkout, portal, webhooks, and plan info."""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.billing.plans import (
    PLAN_FEATURES,
    get_plan_features,
    get_plan_price,
    get_stripe_price_id,
)
from app.billing.stripe_client import StripeClientError, create_checkout_session
from app.billing.stripe_client import create_customer as stripe_create_customer
from app.billing.stripe_client import create_portal_session, handle_webhook
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.tenant import PlanTier
from app.schemas.billing import (
    CheckoutRequest,
    PlanFeatures,
    PlanResponse,
    PortalRequest,
    SubscriptionResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/billing", tags=["billing"])


# ---------------------------------------------------------------------------
# GET /billing/plans — public, no auth required
# ---------------------------------------------------------------------------


@router.get("/plans", response_model=list[PlanResponse])
async def list_plans() -> list[PlanResponse]:
    """List all available plans with pricing and feature details."""
    plans: list[PlanResponse] = []
    for tier in PlanTier:
        features = get_plan_features(tier)
        plans.append(
            PlanResponse(
                name=tier.value,
                price_monthly=get_plan_price(tier),
                features=PlanFeatures(**features),
            )
        )
    return plans


# ---------------------------------------------------------------------------
# GET /billing/subscription — requires tenant context
# ---------------------------------------------------------------------------


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(request: Request) -> SubscriptionResponse:
    """Get the current tenant's subscription status."""
    tenant_id = getattr(request.state, "tenant_id", None)
    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant context required",
        )

    db: AsyncSession = request.state.db
    result = await db.execute(
        select(Subscription).where(Subscription.tenant_id == tenant_id)
    )
    subscription = result.scalar_one_or_none()

    if subscription is None:
        return SubscriptionResponse(
            plan=PlanTier.FREE,
            status=SubscriptionStatus.ACTIVE.value,
        )

    return SubscriptionResponse(
        plan=subscription.plan,
        status=subscription.status.value,
        current_period_start=subscription.current_period_start,
        current_period_end=subscription.current_period_end,
        stripe_customer_id=subscription.stripe_customer_id,
    )


# ---------------------------------------------------------------------------
# POST /billing/checkout — create a Stripe Checkout session
# ---------------------------------------------------------------------------


@router.post("/checkout")
async def create_checkout(request: Request, body: CheckoutRequest) -> dict:
    """Create a Stripe Checkout session for a plan upgrade."""
    tenant_id = getattr(request.state, "tenant_id", None)
    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant context required",
        )

    if body.plan == PlanTier.FREE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot checkout for the free plan",
        )

    price_id = get_stripe_price_id(body.plan)
    if not price_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Price not configured for plan: {body.plan.value}",
        )

    db: AsyncSession = request.state.db
    result = await db.execute(
        select(Subscription).where(Subscription.tenant_id == tenant_id)
    )
    subscription = result.scalar_one_or_none()

    try:
        if subscription is None:
            customer_id = stripe_create_customer(
                email=getattr(request.state, "user_email", ""),
                name=getattr(request.state, "tenant_name", ""),
                tenant_id=str(tenant_id),
            )
        else:
            customer_id = subscription.stripe_customer_id

        url = create_checkout_session(
            customer_id=customer_id,
            price_id=price_id,
            success_url=body.success_url,
            cancel_url=body.cancel_url,
        )
        return {"checkout_url": url}
    except StripeClientError as exc:
        logger.error("Checkout failed for tenant %s: %s", tenant_id, exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Payment provider error. Please try again.",
        ) from exc


# ---------------------------------------------------------------------------
# POST /billing/portal — create a Stripe Customer Portal session
# ---------------------------------------------------------------------------


@router.post("/portal")
async def create_portal(request: Request, body: PortalRequest) -> dict:
    """Create a Stripe Customer Portal session for subscription management."""
    tenant_id = getattr(request.state, "tenant_id", None)
    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant context required",
        )

    db: AsyncSession = request.state.db
    result = await db.execute(
        select(Subscription).where(Subscription.tenant_id == tenant_id)
    )
    subscription = result.scalar_one_or_none()

    if subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active subscription found",
        )

    try:
        url = create_portal_session(
            customer_id=subscription.stripe_customer_id,
            return_url=body.return_url,
        )
        return {"portal_url": url}
    except StripeClientError as exc:
        logger.error("Portal session failed for tenant %s: %s", tenant_id, exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Payment provider error. Please try again.",
        ) from exc


# ---------------------------------------------------------------------------
# POST /billing/webhook — handle Stripe webhook events
# ---------------------------------------------------------------------------


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def stripe_webhook(request: Request) -> dict:
    """Handle incoming Stripe webhook events.

    Processes: customer.subscription.created, updated, deleted.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = handle_webhook(payload, sig_header)
    except StripeClientError as exc:
        logger.warning("Webhook rejected: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook",
        ) from exc

    event_type: str = event.get("type", "")
    event_data: dict = event.get("data", {}).get("object", {})

    logger.info("Processing webhook event: %s", event_type)

    db: AsyncSession = request.state.db

    if event_type in (
        "customer.subscription.created",
        "customer.subscription.updated",
    ):
        await _upsert_subscription(db, event_data)
    elif event_type == "customer.subscription.deleted":
        await _cancel_subscription(db, event_data)
    else:
        logger.debug("Ignoring unhandled webhook event: %s", event_type)

    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_STRIPE_STATUS_MAP: dict[str, SubscriptionStatus] = {
    "active": SubscriptionStatus.ACTIVE,
    "past_due": SubscriptionStatus.PAST_DUE,
    "canceled": SubscriptionStatus.CANCELED,
    "trialing": SubscriptionStatus.TRIALING,
}


async def _upsert_subscription(db: AsyncSession, data: dict) -> None:
    """Create or update a subscription from a Stripe event."""
    stripe_customer_id = data.get("customer", "")
    stripe_sub_id = data.get("id", "")
    stripe_status = data.get("status", "active")

    result = await db.execute(
        select(Subscription).where(
            Subscription.stripe_customer_id == stripe_customer_id
        )
    )
    subscription = result.scalar_one_or_none()

    mapped_status = _STRIPE_STATUS_MAP.get(stripe_status, SubscriptionStatus.ACTIVE)
    period_start = _unix_to_datetime(data.get("current_period_start"))
    period_end = _unix_to_datetime(data.get("current_period_end"))

    # Determine plan from price ID in the first line item
    plan = _resolve_plan_from_data(data)

    if subscription is None:
        tenant_id = _extract_tenant_id(data)
        if tenant_id is None:
            logger.error("Cannot resolve tenant for Stripe customer %s", stripe_customer_id)
            return
        subscription = Subscription(
            tenant_id=tenant_id,
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_sub_id,
            plan=plan,
            status=mapped_status,
            current_period_start=period_start,
            current_period_end=period_end,
        )
        db.add(subscription)
    else:
        subscription.stripe_subscription_id = stripe_sub_id
        subscription.plan = plan
        subscription.status = mapped_status
        subscription.current_period_start = period_start
        subscription.current_period_end = period_end

    await db.commit()
    logger.info("Upserted subscription for customer %s -> %s", stripe_customer_id, plan.value)


async def _cancel_subscription(db: AsyncSession, data: dict) -> None:
    """Mark a subscription as canceled from a Stripe event."""
    stripe_sub_id = data.get("id", "")

    result = await db.execute(
        select(Subscription).where(
            Subscription.stripe_subscription_id == stripe_sub_id
        )
    )
    subscription = result.scalar_one_or_none()

    if subscription is None:
        logger.warning("Received cancellation for unknown subscription %s", stripe_sub_id)
        return

    subscription.status = SubscriptionStatus.CANCELED
    await db.commit()
    logger.info("Canceled subscription %s", stripe_sub_id)


def _unix_to_datetime(ts: int | None) -> datetime | None:
    """Convert a Unix timestamp to a timezone-aware datetime."""
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def _resolve_plan_from_data(data: dict) -> PlanTier:
    """Resolve the PlanTier from Stripe subscription line items."""
    import os

    items = data.get("items", {}).get("data", [])
    if not items:
        return PlanTier.FREE

    price_id = items[0].get("price", {}).get("id", "")

    env_to_plan = {
        os.environ.get("STRIPE_PRICE_STARTER", ""): PlanTier.STARTER,
        os.environ.get("STRIPE_PRICE_PRO", ""): PlanTier.PRO,
        os.environ.get("STRIPE_PRICE_ENTERPRISE", ""): PlanTier.ENTERPRISE,
    }

    return env_to_plan.get(price_id, PlanTier.STARTER)


def _extract_tenant_id(data: dict) -> str | None:
    """Extract tenant_id from Stripe customer metadata via the event data."""
    metadata = data.get("metadata", {})
    return metadata.get("tenant_id")
