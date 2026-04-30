"""Stripe client wrapper — async-compatible interface for Stripe operations."""

import logging
import os
from functools import lru_cache
from typing import Any

import stripe

logger = logging.getLogger(__name__)


class StripeClientError(Exception):
    """Raised when a Stripe operation fails."""


@lru_cache(maxsize=1)
def _get_stripe_secret_key() -> str:
    """Read and cache the Stripe secret key from environment."""
    key = os.environ.get("STRIPE_SECRET_KEY", "")
    if not key:
        raise StripeClientError("STRIPE_SECRET_KEY environment variable is not set")
    return key


def _client() -> stripe.StripeClient:
    """Return a configured Stripe client instance."""
    return stripe.StripeClient(api_key=_get_stripe_secret_key())


def create_customer(email: str, name: str, tenant_id: str) -> str:
    """Create a Stripe customer and return the customer ID.

    Args:
        email: Customer email address.
        name: Customer/organization display name.
        tenant_id: Internal tenant UUID (stored as Stripe metadata).

    Returns:
        Stripe customer ID (e.g. ``cus_...``).

    Raises:
        StripeClientError: If the Stripe API call fails.
    """
    try:
        client = _client()
        customer = client.customers.create(
            params={
                "email": email,
                "name": name,
                "metadata": {"tenant_id": tenant_id},
            }
        )
        logger.info("Created Stripe customer %s for tenant %s", customer.id, tenant_id)
        return customer.id
    except stripe.StripeError as exc:
        logger.error("Failed to create Stripe customer: %s", exc)
        raise StripeClientError(f"Failed to create Stripe customer: {exc}") from exc


def create_checkout_session(
    customer_id: str,
    price_id: str,
    success_url: str,
    cancel_url: str,
) -> str:
    """Create a Stripe Checkout session and return the session URL.

    Args:
        customer_id: Existing Stripe customer ID.
        price_id: Stripe Price ID for the chosen plan.
        success_url: URL to redirect to on success.
        cancel_url: URL to redirect to on cancellation.

    Returns:
        Checkout session URL the client should redirect to.

    Raises:
        StripeClientError: If the Stripe API call fails.
    """
    try:
        client = _client()
        session = client.checkout.sessions.create(
            params={
                "customer": customer_id,
                "mode": "subscription",
                "line_items": [{"price": price_id, "quantity": 1}],
                "success_url": success_url,
                "cancel_url": cancel_url,
            }
        )
        logger.info("Created checkout session %s for customer %s", session.id, customer_id)
        return session.url or ""
    except stripe.StripeError as exc:
        logger.error("Failed to create checkout session: %s", exc)
        raise StripeClientError(f"Failed to create checkout session: {exc}") from exc


def create_portal_session(customer_id: str, return_url: str) -> str:
    """Create a Stripe Customer Portal session and return the URL.

    Args:
        customer_id: Existing Stripe customer ID.
        return_url: URL to return to after the portal session.

    Returns:
        Customer portal session URL.

    Raises:
        StripeClientError: If the Stripe API call fails.
    """
    try:
        client = _client()
        session = client.billing_portal.sessions.create(
            params={
                "customer": customer_id,
                "return_url": return_url,
            }
        )
        logger.info("Created portal session for customer %s", customer_id)
        return session.url
    except stripe.StripeError as exc:
        logger.error("Failed to create portal session: %s", exc)
        raise StripeClientError(f"Failed to create portal session: {exc}") from exc


def handle_webhook(payload: bytes, sig_header: str) -> dict[str, Any]:
    """Verify and parse a Stripe webhook event.

    Args:
        payload: Raw request body bytes.
        sig_header: Value of the ``Stripe-Signature`` header.

    Returns:
        Parsed webhook event as a dictionary with ``type`` and ``data`` keys.

    Raises:
        StripeClientError: If signature verification fails or payload is invalid.
    """
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    if not webhook_secret:
        raise StripeClientError("STRIPE_WEBHOOK_SECRET environment variable is not set")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        logger.info("Received webhook event: %s (id=%s)", event["type"], event["id"])
        return dict(event)
    except stripe.SignatureVerificationError as exc:
        logger.error("Webhook signature verification failed: %s", exc)
        raise StripeClientError("Invalid webhook signature") from exc
    except ValueError as exc:
        logger.error("Invalid webhook payload: %s", exc)
        raise StripeClientError("Invalid webhook payload") from exc
