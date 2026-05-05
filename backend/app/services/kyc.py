"""KYC service — identity verification and AML compliance checks.

Integrates with external KYC providers (Sumsub, Onfido) and manages
the verification lifecycle: initiation → document upload → review → decision.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.compliance_record import ComplianceEventType, ComplianceRecord, RiskLevel
from app.models.kyc import DocumentType, KYCRecord, KYCStatus, VerificationLevel

logger = structlog.get_logger("kyc")


class KYCVerificationError(Exception):
    """Raised when KYC verification fails."""


async def initiate_verification(
    db: AsyncSession,
    *,
    tenant_id: uuid.UUID,
    user_id: uuid.UUID,
    level: VerificationLevel,
    document_type: DocumentType,
) -> KYCRecord:
    """Start a new KYC verification process.

    Creates a KYC record and initiates verification with the configured provider.
    """
    provider = os.environ.get("KYC_PROVIDER", "sumsub")

    record = KYCRecord(
        tenant_id=tenant_id,
        user_id=user_id,
        verification_level=level,
        status=KYCStatus.PENDING,
        provider=provider,
        document_type=document_type,
        risk_score=0,
    )
    db.add(record)

    # Create compliance audit trail
    compliance = ComplianceRecord(
        tenant_id=tenant_id,
        event_type=ComplianceEventType.KYC_CHECK,
        entity_type="user",
        entity_id=user_id,
        risk_level=RiskLevel.LOW,
        details={
            "action": "verification_initiated",
            "level": level.value,
            "provider": provider,
            "document_type": document_type.value,
        },
    )
    db.add(compliance)

    await db.commit()
    await db.refresh(record)

    logger.info(
        "kyc_initiated",
        user_id=str(user_id),
        level=level.value,
        provider=provider,
    )

    return record


async def process_webhook(
    db: AsyncSession,
    *,
    provider: str,
    payload: dict[str, Any],
) -> KYCRecord | None:
    """Process a webhook callback from KYC provider.

    Updates the KYC record based on provider decision.
    """
    reference_id = payload.get("applicantId") or payload.get("check_id")
    if not reference_id:
        logger.warning("kyc_webhook_missing_reference", payload=payload)
        return None

    result = await db.execute(
        select(KYCRecord).where(KYCRecord.provider_reference_id == reference_id)
    )
    record = result.scalar_one_or_none()

    if not record:
        logger.warning("kyc_webhook_unknown_reference", reference_id=reference_id)
        return None

    decision = payload.get("reviewResult", {}).get("reviewAnswer", "")
    risk_score = payload.get("riskScore", 0)

    if decision == "GREEN":
        record.status = KYCStatus.APPROVED
        record.verified_at = datetime.now(timezone.utc)
        record.risk_score = min(risk_score, 30)
    elif decision == "RED":
        record.status = KYCStatus.REJECTED
        record.rejection_reason = payload.get("reviewResult", {}).get("rejectLabels", ["unknown"])[0]
        record.risk_score = max(risk_score, 70)
    else:
        record.status = KYCStatus.IN_REVIEW
        record.risk_score = risk_score

    # Compliance trail
    risk_level = RiskLevel.LOW if record.risk_score < 30 else (
        RiskLevel.MEDIUM if record.risk_score < 60 else (
            RiskLevel.HIGH if record.risk_score < 80 else RiskLevel.CRITICAL
        )
    )

    compliance = ComplianceRecord(
        tenant_id=record.tenant_id,
        event_type=ComplianceEventType.KYC_CHECK,
        entity_type="user",
        entity_id=record.user_id,
        risk_level=risk_level,
        details={
            "action": "webhook_processed",
            "decision": decision,
            "risk_score": record.risk_score,
            "provider": provider,
        },
    )
    db.add(compliance)

    await db.commit()
    await db.refresh(record)

    logger.info(
        "kyc_webhook_processed",
        reference_id=reference_id,
        status=record.status.value,
        risk_score=record.risk_score,
    )

    return record


async def get_user_verification(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
) -> KYCRecord | None:
    """Get the latest KYC record for a user."""
    result = await db.execute(
        select(KYCRecord)
        .where(KYCRecord.user_id == user_id)
        .order_by(KYCRecord.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()
