"""KYC API — identity verification and compliance status."""

import uuid

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.kyc import DocumentType, KYCStatus, VerificationLevel
from app.services.kyc import get_user_verification, initiate_verification, process_webhook

router = APIRouter(prefix="/kyc", tags=["kyc"])


# ─── Schemas ────────────────────────────────────────────────────────────


class KYCStatusResponse(BaseModel):
    id: str | None
    verification_level: str
    status: str
    risk_score: int
    verified_at: str | None


class InitiateKYCRequest(BaseModel):
    level: VerificationLevel = VerificationLevel.BASIC
    document_type: DocumentType = DocumentType.PASSPORT


class KYCWebhookPayload(BaseModel):
    applicantId: str | None = None
    check_id: str | None = None
    reviewResult: dict | None = None
    riskScore: int = 0


# ─── Endpoints ──────────────────────────────────────────────────────────


@router.get("/status", response_model=KYCStatusResponse)
async def get_kyc_status(request: Request) -> KYCStatusResponse:
    """Get the current user's KYC verification status."""
    user_id = _require_user(request)
    db: AsyncSession = request.state.db

    record = await get_user_verification(db, user_id=user_id)

    if record is None:
        return KYCStatusResponse(
            id=None,
            verification_level=VerificationLevel.NONE.value,
            status=KYCStatus.PENDING.value,
            risk_score=0,
            verified_at=None,
        )

    return KYCStatusResponse(
        id=str(record.id),
        verification_level=record.verification_level,
        status=record.status,
        risk_score=record.risk_score,
        verified_at=record.verified_at.isoformat() if record.verified_at else None,
    )


@router.post("/verify", response_model=KYCStatusResponse, status_code=status.HTTP_201_CREATED)
async def start_verification(request: Request, body: InitiateKYCRequest) -> KYCStatusResponse:
    """Initiate a KYC verification process for the current user."""
    tenant_id = _require_tenant(request)
    user_id = _require_user(request)
    db: AsyncSession = request.state.db

    # Check if user already has a pending/approved verification
    existing = await get_user_verification(db, user_id=user_id)
    if existing and existing.status in (KYCStatus.PENDING, KYCStatus.IN_REVIEW, KYCStatus.APPROVED):
        raise HTTPException(
            status_code=400,
            detail=f"Verification already {existing.status.value}. Cannot start a new one.",
        )

    record = await initiate_verification(
        db,
        tenant_id=tenant_id,
        user_id=user_id,
        level=body.level,
        document_type=body.document_type,
    )

    return KYCStatusResponse(
        id=str(record.id),
        verification_level=record.verification_level,
        status=record.status,
        risk_score=record.risk_score,
        verified_at=None,
    )


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def kyc_webhook(request: Request) -> dict:
    """Handle KYC provider webhook callbacks (Sumsub, Onfido).

    Verifies HMAC signature before processing. Rejects unsigned requests.
    """
    import hashlib
    import hmac
    import os

    raw_body = await request.body()
    signature = request.headers.get("x-payload-digest", "")
    webhook_secret = os.environ.get("SUMSUB_WEBHOOK_SECRET", "")

    if not webhook_secret:
        raise HTTPException(status_code=503, detail="Webhook secret not configured")

    expected = hmac.new(
        webhook_secret.encode(), raw_body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=403, detail="Invalid webhook signature")

    import json
    payload = json.loads(raw_body)
    db: AsyncSession = request.state.db

    allowed_providers = {"sumsub", "onfido"}
    provider = request.headers.get("x-provider", "sumsub")
    if provider not in allowed_providers:
        raise HTTPException(status_code=400, detail="Unknown provider")

    await process_webhook(db, provider=provider, payload=payload)

    return {"status": "ok"}


# ─── Helpers ────────────────────────────────────────────────────────────


def _require_tenant(request: Request) -> uuid.UUID:
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(status_code=401, detail="Tenant context required")
    return tenant_id


def _require_user(request: Request) -> uuid.UUID:
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id
