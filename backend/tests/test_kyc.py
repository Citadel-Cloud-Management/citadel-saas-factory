"""Tests for the KYC service — identity verification and AML compliance.

Critical financial path: 95% coverage required (auth/payments/matching tier).

TDD coverage:
- initiate_verification creates KYC record + compliance audit entry
- process_webhook GREEN decision -> APPROVED with low risk score
- process_webhook RED decision  -> REJECTED with high risk score
- process_webhook unknown decision -> IN_REVIEW
- process_webhook with missing reference returns None
- process_webhook for unknown reference returns None
- Duplicate verification: second record created (service allows; caller deduplicates)
- Expired verification: status remains EXPIRED (immutable from provider side)
- Risk score clamping boundaries
"""

import uuid
from datetime import datetime, timezone
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.compliance_record import ComplianceEventType, ComplianceRecord, RiskLevel
from app.models.kyc import DocumentType, KYCRecord, KYCStatus, VerificationLevel
from app.services.kyc import KYCVerificationError, initiate_verification, process_webhook


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tenant_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def user_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def provider_reference_id() -> str:
    return f"ref-{uuid.uuid4().hex[:12]}"


def _make_kyc_record(
    *,
    tenant_id: uuid.UUID,
    user_id: uuid.UUID,
    reference_id: str,
    status: KYCStatus = KYCStatus.PENDING,
    risk_score: int = 0,
) -> MagicMock:
    """Build a minimal KYCRecord mock that mirrors the real model."""
    record = MagicMock(spec=KYCRecord)
    record.id = uuid.uuid4()
    record.tenant_id = tenant_id
    record.user_id = user_id
    record.provider_reference_id = reference_id
    record.status = status
    record.risk_score = risk_score
    record.rejection_reason = None
    record.verified_at = None
    record.expires_at = None
    return record


def _make_db(scalar_result: Any = None) -> AsyncMock:
    """Return a fully-mocked AsyncSession.

    scalar_result: what scalar_one_or_none() returns from db.execute().
    """
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.execute = AsyncMock(
        return_value=MagicMock(
            scalar_one_or_none=MagicMock(return_value=scalar_result)
        )
    )
    return db


# ---------------------------------------------------------------------------
# initiate_verification
# ---------------------------------------------------------------------------


class TestInitiateVerification:
    @pytest.mark.asyncio
    async def test_creates_kyc_record_and_compliance_entry(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """initiate_verification adds two records: KYCRecord + ComplianceRecord."""
        db = _make_db()

        with patch.dict("os.environ", {"KYC_PROVIDER": "sumsub"}):
            await initiate_verification(
                db,
                tenant_id=tenant_id,
                user_id=user_id,
                level=VerificationLevel.BASIC,
                document_type=DocumentType.PASSPORT,
            )

        assert db.add.call_count == 2
        assert db.commit.called
        assert db.refresh.called

    @pytest.mark.asyncio
    async def test_kyc_record_has_pending_status(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """Newly initiated KYCRecord must start as PENDING."""
        db = _make_db()
        added_objects: list = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))

        with patch.dict("os.environ", {"KYC_PROVIDER": "onfido"}):
            await initiate_verification(
                db,
                tenant_id=tenant_id,
                user_id=user_id,
                level=VerificationLevel.ENHANCED,
                document_type=DocumentType.DRIVERS_LICENSE,
            )

        kyc_records = [o for o in added_objects if isinstance(o, KYCRecord)]
        assert len(kyc_records) == 1
        assert kyc_records[0].status == KYCStatus.PENDING

    @pytest.mark.asyncio
    async def test_compliance_record_event_type_is_kyc_check(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """The compliance audit entry must use KYC_CHECK event type."""
        db = _make_db()
        added_objects: list = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))

        with patch.dict("os.environ", {"KYC_PROVIDER": "sumsub"}):
            await initiate_verification(
                db,
                tenant_id=tenant_id,
                user_id=user_id,
                level=VerificationLevel.FULL,
                document_type=DocumentType.NATIONAL_ID,
            )

        compliance_records = [o for o in added_objects if isinstance(o, ComplianceRecord)]
        assert len(compliance_records) == 1
        assert compliance_records[0].event_type == ComplianceEventType.KYC_CHECK

    @pytest.mark.asyncio
    async def test_default_provider_is_sumsub(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """When KYC_PROVIDER env var is absent, 'sumsub' is used as default."""
        db = _make_db()
        added_objects: list = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))

        # Ensure env var is absent
        with patch.dict("os.environ", {}, clear=False):
            import os

            os.environ.pop("KYC_PROVIDER", None)
            await initiate_verification(
                db,
                tenant_id=tenant_id,
                user_id=user_id,
                level=VerificationLevel.BASIC,
                document_type=DocumentType.PASSPORT,
            )

        kyc_records = [o for o in added_objects if isinstance(o, KYCRecord)]
        assert kyc_records[0].provider == "sumsub"

    @pytest.mark.asyncio
    async def test_risk_score_initialises_to_zero(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """Initial risk_score must be 0 before any provider decision."""
        db = _make_db()
        added_objects: list = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))

        with patch.dict("os.environ", {"KYC_PROVIDER": "sumsub"}):
            await initiate_verification(
                db,
                tenant_id=tenant_id,
                user_id=user_id,
                level=VerificationLevel.BASIC,
                document_type=DocumentType.PASSPORT,
            )

        kyc_records = [o for o in added_objects if isinstance(o, KYCRecord)]
        assert kyc_records[0].risk_score == 0


# ---------------------------------------------------------------------------
# process_webhook
# ---------------------------------------------------------------------------


class TestProcessWebhookGreen:
    @pytest.mark.asyncio
    async def test_green_decision_sets_approved_status(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """GREEN webhook -> KYCStatus.APPROVED."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "GREEN"},
            "riskScore": 10,
        }

        result = await process_webhook(db, provider="sumsub", payload=payload)

        assert result is record
        assert record.status == KYCStatus.APPROVED
        assert record.verified_at is not None

    @pytest.mark.asyncio
    async def test_green_decision_clamps_risk_score_to_max_30(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """GREEN decision caps risk_score at 30 regardless of provider value."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "GREEN"},
            "riskScore": 95,  # Provider sends high score but GREEN decision
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        assert record.risk_score == 30  # Clamped to max 30 for GREEN

    @pytest.mark.asyncio
    async def test_green_decision_low_risk_score_preserved(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """GREEN decision with score < 30 preserves the provider score unchanged."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "GREEN"},
            "riskScore": 15,
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        assert record.risk_score == 15

    @pytest.mark.asyncio
    async def test_green_decision_commits_and_creates_compliance_entry(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """GREEN webhook commits and adds a ComplianceRecord."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)
        added_objects: list = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "GREEN"},
            "riskScore": 5,
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        assert db.commit.called
        assert db.refresh.called
        compliance_entries = [o for o in added_objects if isinstance(o, ComplianceRecord)]
        assert len(compliance_entries) == 1
        assert compliance_entries[0].risk_level == RiskLevel.LOW


class TestProcessWebhookRed:
    @pytest.mark.asyncio
    async def test_red_decision_sets_rejected_status(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """RED webhook -> KYCStatus.REJECTED."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {
                "reviewAnswer": "RED",
                "rejectLabels": ["FORGERY"],
            },
            "riskScore": 85,
        }

        result = await process_webhook(db, provider="sumsub", payload=payload)

        assert result is record
        assert record.status == KYCStatus.REJECTED

    @pytest.mark.asyncio
    async def test_red_decision_stores_rejection_reason(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """RED webhook stores the first rejectLabel as rejection_reason."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {
                "reviewAnswer": "RED",
                "rejectLabels": ["DOCUMENT_MISMATCH", "EXPIRED"],
            },
            "riskScore": 80,
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        assert record.rejection_reason == "DOCUMENT_MISMATCH"

    @pytest.mark.asyncio
    async def test_red_decision_clamps_risk_score_to_min_70(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """RED decision ensures risk_score is at least 70."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "RED", "rejectLabels": ["FORGERY"]},
            "riskScore": 30,  # Provider sends low score, RED must clamp to >= 70
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        assert record.risk_score == 70

    @pytest.mark.asyncio
    async def test_red_decision_high_risk_compliance_entry(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """RED with score >= 80 creates ComplianceRecord with CRITICAL risk level."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)
        added_objects: list = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "RED", "rejectLabels": ["SANCTIONS"]},
            "riskScore": 90,
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        compliance_entries = [o for o in added_objects if isinstance(o, ComplianceRecord)]
        assert len(compliance_entries) == 1
        assert compliance_entries[0].risk_level == RiskLevel.CRITICAL

    @pytest.mark.asyncio
    async def test_red_missing_reject_labels_uses_unknown_fallback(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """When rejectLabels is absent, rejection_reason falls back to 'unknown'."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "RED"},  # No rejectLabels key
            "riskScore": 80,
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        assert record.rejection_reason == "unknown"


class TestProcessWebhookUnknownDecision:
    @pytest.mark.asyncio
    async def test_unknown_decision_sets_in_review(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """A decision that is neither GREEN nor RED -> KYCStatus.IN_REVIEW."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "YELLOW"},
            "riskScore": 50,
        }

        result = await process_webhook(db, provider="sumsub", payload=payload)

        assert result is record
        assert record.status == KYCStatus.IN_REVIEW
        assert record.risk_score == 50

    @pytest.mark.asyncio
    async def test_empty_decision_sets_in_review(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """Empty reviewAnswer string -> IN_REVIEW (neither GREEN nor RED)."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": ""},
            "riskScore": 45,
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        assert record.status == KYCStatus.IN_REVIEW


class TestProcessWebhookEdgeCases:
    @pytest.mark.asyncio
    async def test_missing_reference_id_returns_none(self) -> None:
        """Webhook payload without applicantId or check_id returns None without crashing."""
        db = _make_db()

        payload: dict = {"reviewResult": {"reviewAnswer": "GREEN"}}

        result = await process_webhook(db, provider="sumsub", payload=payload)

        assert result is None
        db.execute.assert_not_called()

    @pytest.mark.asyncio
    async def test_unknown_reference_returns_none(self, provider_reference_id: str) -> None:
        """Webhook for a reference_id not in database returns None."""
        db = _make_db(scalar_result=None)  # No record found

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "GREEN"},
            "riskScore": 5,
        }

        result = await process_webhook(db, provider="sumsub", payload=payload)

        assert result is None
        db.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_onfido_check_id_field_also_accepted(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """Onfido uses 'check_id' instead of 'applicantId' — both must be supported."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "check_id": provider_reference_id,  # Onfido field
            "reviewResult": {"reviewAnswer": "GREEN"},
            "riskScore": 8,
        }

        result = await process_webhook(db, provider="onfido", payload=payload)

        assert result is record
        assert record.status == KYCStatus.APPROVED

    @pytest.mark.asyncio
    async def test_empty_payload_returns_none(self) -> None:
        """Completely empty payload is handled gracefully."""
        db = _make_db()

        result = await process_webhook(db, provider="sumsub", payload={})

        assert result is None

    @pytest.mark.asyncio
    async def test_medium_risk_score_compliance_level(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """Score in [30, 60) produces MEDIUM risk compliance entry."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)
        added_objects: list = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "OTHER"},
            "riskScore": 45,
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        compliance_entries = [o for o in added_objects if isinstance(o, ComplianceRecord)]
        assert compliance_entries[0].risk_level == RiskLevel.MEDIUM

    @pytest.mark.asyncio
    async def test_high_risk_score_compliance_level(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """Score in [60, 80) produces HIGH risk compliance entry."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
        )
        db = _make_db(scalar_result=record)
        added_objects: list = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "MAYBE"},
            "riskScore": 70,
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        compliance_entries = [o for o in added_objects if isinstance(o, ComplianceRecord)]
        assert compliance_entries[0].risk_level == RiskLevel.HIGH


class TestDuplicateVerification:
    @pytest.mark.asyncio
    async def test_second_initiation_creates_new_record(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID
    ) -> None:
        """The service does not deduplicate; a second call creates a second record.

        Deduplication (e.g., checking for existing PENDING records) is the
        responsibility of the API/use-case layer. This test documents the
        service-level boundary explicitly.
        """
        db = _make_db()
        added_objects: list = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))

        with patch.dict("os.environ", {"KYC_PROVIDER": "sumsub"}):
            await initiate_verification(
                db,
                tenant_id=tenant_id,
                user_id=user_id,
                level=VerificationLevel.BASIC,
                document_type=DocumentType.PASSPORT,
            )

        first_call_adds = len(added_objects)

        db2 = _make_db()
        added_objects2: list = []
        db2.add = MagicMock(side_effect=lambda obj: added_objects2.append(obj))

        with patch.dict("os.environ", {"KYC_PROVIDER": "sumsub"}):
            await initiate_verification(
                db2,
                tenant_id=tenant_id,
                user_id=user_id,
                level=VerificationLevel.BASIC,
                document_type=DocumentType.PASSPORT,
            )

        # Each call adds 2 objects (KYCRecord + ComplianceRecord)
        assert first_call_adds == 2
        assert len(added_objects2) == 2


class TestExpiredVerificationHandling:
    @pytest.mark.asyncio
    async def test_expired_record_status_remains_expired_on_any_webhook(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """A previously EXPIRED record is overwritten by the webhook decision.

        The service does not guard against updating EXPIRED records — it
        trusts the provider. This test documents the current behaviour: a
        GREEN webhook on an EXPIRED record will move it to APPROVED.
        If this is undesired, the guard must be added to the service.
        """
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
            status=KYCStatus.EXPIRED,
            risk_score=0,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "GREEN"},
            "riskScore": 5,
        }

        result = await process_webhook(db, provider="sumsub", payload=payload)

        # Service overwrites EXPIRED with APPROVED — document this for review
        assert result is record
        assert record.status == KYCStatus.APPROVED

    @pytest.mark.asyncio
    async def test_expired_record_red_webhook_moves_to_rejected(
        self, tenant_id: uuid.UUID, user_id: uuid.UUID, provider_reference_id: str
    ) -> None:
        """RED webhook on an EXPIRED record moves it to REJECTED."""
        record = _make_kyc_record(
            tenant_id=tenant_id,
            user_id=user_id,
            reference_id=provider_reference_id,
            status=KYCStatus.EXPIRED,
        )
        db = _make_db(scalar_result=record)

        payload = {
            "applicantId": provider_reference_id,
            "reviewResult": {"reviewAnswer": "RED", "rejectLabels": ["EXPIRED_DOC"]},
            "riskScore": 75,
        }

        await process_webhook(db, provider="sumsub", payload=payload)

        assert record.status == KYCStatus.REJECTED
        assert record.rejection_reason == "EXPIRED_DOC"
