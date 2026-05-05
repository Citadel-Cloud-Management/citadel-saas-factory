"""Celery tasks — email, webhooks, compliance, scheduled jobs."""

import logging
from datetime import datetime, timezone

from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(queue="email", max_retries=3, default_retry_delay=60)
def send_email_task(to: str, subject: str, template: str, context: dict) -> dict:
    """Send an email asynchronously via the email service."""
    logger.info("Sending email to=%s subject=%s template=%s", to, subject, template)
    # In production: calls app.email.service.send()
    return {"status": "sent", "to": to, "template": template}


@celery_app.task(queue="email")
def send_transaction_receipt(transaction_id: str, user_email: str, amount: str, currency: str) -> dict:
    """Send transaction receipt email after successful transfer."""
    return send_email_task(
        to=user_email,
        subject=f"Transaction Confirmed — {amount} {currency}",
        template="transaction_receipt",
        context={"transaction_id": transaction_id, "amount": amount, "currency": currency},
    )


@celery_app.task(queue="email")
def send_kyc_status_update(user_email: str, status: str, level: str) -> dict:
    """Notify user of KYC verification status change."""
    subject_map = {
        "approved": "KYC Verification Approved",
        "rejected": "KYC Verification — Action Required",
        "expired": "KYC Verification Expired — Please Reverify",
    }
    return send_email_task(
        to=user_email,
        subject=subject_map.get(status, f"KYC Status: {status}"),
        template="kyc_status",
        context={"status": status, "level": level},
    )


@celery_app.task(queue="compliance")
def run_aml_batch_screening(tenant_id: str) -> dict:
    """Run batch AML screening for all active users in a tenant."""
    logger.info("Running batch AML screening for tenant=%s", tenant_id)
    # In production: iterate users, check sanctions lists
    return {"tenant_id": tenant_id, "screened_at": datetime.now(timezone.utc).isoformat()}


@celery_app.task(queue="compliance")
def check_kyc_expirations() -> dict:
    """Check for KYC records about to expire and send reminder emails."""
    logger.info("Checking KYC expirations")
    # In production: query kyc_records where expires_at < now + 30 days
    return {"checked_at": datetime.now(timezone.utc).isoformat()}


@celery_app.task(queue="compliance")
def generate_compliance_report() -> dict:
    """Generate daily compliance report (CTRs filed, SARs triggered, alerts)."""
    logger.info("Generating daily compliance report")
    return {"generated_at": datetime.now(timezone.utc).isoformat()}


@celery_app.task(queue="default")
def cleanup_expired_sessions() -> dict:
    """Remove expired sessions from Redis."""
    logger.info("Cleaning up expired sessions")
    return {"cleaned_at": datetime.now(timezone.utc).isoformat()}


@celery_app.task(queue="webhooks", max_retries=5, default_retry_delay=30)
def dispatch_webhook(url: str, event_type: str, payload: dict) -> dict:
    """Dispatch a webhook to a subscriber URL with retry."""
    import httpx

    logger.info("Dispatching webhook type=%s url=%s", event_type, url)
    try:
        response = httpx.post(url, json={"type": event_type, "data": payload}, timeout=10.0)
        response.raise_for_status()
        return {"status": "delivered", "url": url, "status_code": response.status_code}
    except Exception as exc:
        logger.warning("Webhook delivery failed url=%s error=%s", url, exc)
        raise dispatch_webhook.retry(exc=exc)
