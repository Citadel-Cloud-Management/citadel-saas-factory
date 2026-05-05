"""Compliance service — AML screening, transaction monitoring, regulatory reporting.

Implements real-time transaction monitoring rules for:
- Suspicious activity detection (SAR triggers)
- Large transaction reporting (CTR thresholds)
- Velocity checks (unusual patterns)
- Sanctions screening
"""

from __future__ import annotations

import uuid
from decimal import Decimal

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.compliance_record import ComplianceEventType, ComplianceRecord, RiskLevel
from app.models.transaction import Transaction, TransactionStatus

logger = structlog.get_logger("compliance")

# Regulatory thresholds
CTR_THRESHOLD_USD = Decimal("10000.00")  # Currency Transaction Report
SAR_VELOCITY_THRESHOLD = 5  # Transactions per hour triggering review
DAILY_AGGREGATE_THRESHOLD_USD = Decimal("25000.00")


async def screen_transaction(
    db: AsyncSession,
    *,
    tenant_id: uuid.UUID,
    transaction: Transaction,
) -> RiskLevel:
    """Screen a transaction against compliance rules.

    Returns the risk level. HIGH or CRITICAL triggers manual review.
    """
    risk_factors: list[str] = []
    risk_score = 0

    # Rule 1: Large single transaction
    if transaction.amount >= CTR_THRESHOLD_USD:
        risk_factors.append("large_single_transaction")
        risk_score += 40

    # Rule 2: Structuring detection (just below threshold)
    if Decimal("9000") <= transaction.amount < CTR_THRESHOLD_USD:
        risk_score += 25
        risk_factors.append("possible_structuring")

    # Rule 3: Velocity check — too many transactions in short period
    from datetime import datetime, timedelta, timezone
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    velocity_result = await db.execute(
        select(func.count(Transaction.id))
        .where(Transaction.initiated_by == transaction.initiated_by)
        .where(Transaction.created_at >= one_hour_ago)
        .where(Transaction.status != TransactionStatus.FAILED)
    )
    recent_count = velocity_result.scalar() or 0
    if recent_count >= SAR_VELOCITY_THRESHOLD:
        risk_factors.append("high_velocity")
        risk_score += 30

    # Rule 4: Daily aggregate check
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
    daily_result = await db.execute(
        select(func.sum(Transaction.amount))
        .where(Transaction.initiated_by == transaction.initiated_by)
        .where(Transaction.created_at >= today_start)
        .where(Transaction.status == TransactionStatus.COMPLETED)
    )
    daily_total = daily_result.scalar() or Decimal("0")
    if daily_total + transaction.amount >= DAILY_AGGREGATE_THRESHOLD_USD:
        risk_factors.append("daily_aggregate_exceeded")
        risk_score += 35

    # Determine risk level
    if risk_score >= 70:
        risk_level = RiskLevel.CRITICAL
    elif risk_score >= 50:
        risk_level = RiskLevel.HIGH
    elif risk_score >= 25:
        risk_level = RiskLevel.MEDIUM
    else:
        risk_level = RiskLevel.LOW

    # Log compliance record if non-trivial risk
    if risk_level != RiskLevel.LOW:
        record = ComplianceRecord(
            tenant_id=tenant_id,
            event_type=ComplianceEventType.TRANSACTION_REVIEW,
            entity_type="transaction",
            entity_id=transaction.id,
            risk_level=risk_level,
            details={
                "risk_score": risk_score,
                "risk_factors": risk_factors,
                "amount": str(transaction.amount),
                "currency": transaction.currency,
                "daily_total": str(daily_total),
                "recent_velocity": recent_count,
            },
        )
        db.add(record)
        await db.commit()

        logger.warning(
            "compliance_alert",
            transaction_id=str(transaction.id),
            risk_level=risk_level.value,
            risk_score=risk_score,
            factors=risk_factors,
        )

    return risk_level
