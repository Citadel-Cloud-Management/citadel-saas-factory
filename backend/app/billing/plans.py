"""Plan configuration — maps PlanTier to Stripe price IDs and feature limits."""

import os
from typing import Any

from app.models.tenant import PlanTier

# ---------------------------------------------------------------------------
# Stripe Price ID mapping (read from environment at import time is avoided;
# instead we read lazily so tests can patch env vars).
# ---------------------------------------------------------------------------


def _get_price_id(env_var: str) -> str | None:
    """Read a Stripe price ID from environment, returning None if unset."""
    return os.environ.get(env_var) or None


def get_stripe_price_id(plan: PlanTier) -> str | None:
    """Return the Stripe Price ID for a given plan tier.

    Free tier has no price ID (returns ``None``).
    """
    price_map: dict[PlanTier, str | None] = {
        PlanTier.FREE: None,
        PlanTier.STARTER: _get_price_id("STRIPE_PRICE_STARTER"),
        PlanTier.PRO: _get_price_id("STRIPE_PRICE_PRO"),
        PlanTier.ENTERPRISE: _get_price_id("STRIPE_PRICE_ENTERPRISE"),
    }
    return price_map.get(plan)


# ---------------------------------------------------------------------------
# Feature limits per plan
# ---------------------------------------------------------------------------

PLAN_FEATURES: dict[PlanTier, dict[str, Any]] = {
    PlanTier.FREE: {
        "max_users": 3,
        "max_agents": 5,
        "max_storage_gb": 1,
        "api_rate_limit": 100,
        "support": "community",
        "custom_domain": False,
        "sso": False,
        "audit_log": False,
    },
    PlanTier.STARTER: {
        "max_users": 10,
        "max_agents": 25,
        "max_storage_gb": 10,
        "api_rate_limit": 1_000,
        "support": "email",
        "custom_domain": False,
        "sso": False,
        "audit_log": True,
    },
    PlanTier.PRO: {
        "max_users": 50,
        "max_agents": 100,
        "max_storage_gb": 100,
        "api_rate_limit": 10_000,
        "support": "priority",
        "custom_domain": True,
        "sso": True,
        "audit_log": True,
    },
    PlanTier.ENTERPRISE: {
        "max_users": -1,  # unlimited
        "max_agents": -1,  # unlimited
        "max_storage_gb": -1,  # unlimited
        "api_rate_limit": -1,  # unlimited
        "support": "dedicated",
        "custom_domain": True,
        "sso": True,
        "audit_log": True,
    },
}

PLAN_PRICING: dict[PlanTier, int] = {
    PlanTier.FREE: 0,
    PlanTier.STARTER: 29,
    PlanTier.PRO: 99,
    PlanTier.ENTERPRISE: 299,
}


def get_plan_features(plan: PlanTier) -> dict[str, Any]:
    """Return the feature limits for a given plan tier.

    Returns a *copy* to prevent mutation of the module-level constant.
    """
    features = PLAN_FEATURES.get(plan)
    if features is None:
        return {}
    return {**features}


def get_plan_price(plan: PlanTier) -> int:
    """Return monthly price in USD for a plan tier."""
    return PLAN_PRICING.get(plan, 0)
