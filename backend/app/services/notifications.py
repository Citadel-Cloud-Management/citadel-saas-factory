"""Notification service — unified email + WebSocket + push notifications."""

from __future__ import annotations

import logging
import uuid
from typing import Any

logger = logging.getLogger(__name__)


class NotificationService:
    """Dispatches notifications across channels based on event type."""

    async def notify_transaction_complete(
        self, user_id: uuid.UUID, email: str, transaction_id: str, amount: str, currency: str,
    ) -> None:
        """Notify user of completed transaction via email + WebSocket."""
        from app.workers.tasks import send_transaction_receipt
        from app.api.v1.ws import get_ws_manager

        # Email (async via Celery)
        send_transaction_receipt.delay(transaction_id, email, amount, currency)

        # WebSocket (real-time)
        ws = get_ws_manager()
        await ws.send_to_user(str(user_id), "transaction.completed", {
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
        })

        logger.info("Notified user=%s transaction=%s", user_id, transaction_id)

    async def notify_kyc_status(
        self, user_id: uuid.UUID, email: str, status: str, level: str,
    ) -> None:
        """Notify user of KYC status change."""
        from app.workers.tasks import send_kyc_status_update
        from app.api.v1.ws import get_ws_manager

        send_kyc_status_update.delay(email, status, level)

        ws = get_ws_manager()
        await ws.send_to_user(str(user_id), "kyc.status_changed", {
            "status": status,
            "level": level,
        })

    async def notify_compliance_alert(
        self, user_id: uuid.UUID, risk_level: str, details: dict[str, Any],
    ) -> None:
        """Push compliance alert to user's WebSocket connection."""
        from app.api.v1.ws import get_ws_manager

        ws = get_ws_manager()
        await ws.send_to_user(str(user_id), "compliance.alert", {
            "risk_level": risk_level,
            "details": details,
        })

    async def notify_balance_update(
        self, user_id: uuid.UUID, account_id: str, new_balance: str, currency: str,
    ) -> None:
        """Push balance change to user's WebSocket."""
        from app.api.v1.ws import get_ws_manager

        ws = get_ws_manager()
        await ws.send_to_user(str(user_id), "balance.updated", {
            "account_id": account_id,
            "balance": new_balance,
            "currency": currency,
        })


# Singleton
notifications = NotificationService()
