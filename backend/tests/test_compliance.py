"""Tests for the compliance screening service — AML/CTR/SAR rules."""

import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.compliance_record import RiskLevel
from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.services.compliance import (
    CTR_THRESHOLD_USD,
    DAILY_AGGREGATE_THRESHOLD_USD,
    SAR_VELOCITY_THRESHOLD,
    screen_transaction,
)


@pytest.fixture
def tenant_id():
    return uuid.uuid4()


@pytest.fixture
def user_id():
    return uuid.uuid4()


@pytest.fixture
def small_transaction(tenant_id, user_id):
    """A normal small transaction — should pass with LOW risk."""
    txn = MagicMock(spec=Transaction)
    txn.id = uuid.uuid4()
    txn.tenant_id = tenant_id
    txn.amount = Decimal("50.00")
    txn.currency = "USD"
    txn.initiated_by = user_id
    txn.status = TransactionStatus.COMPLETED
    txn.created_at = MagicMock()
    return txn


@pytest.fixture
def large_transaction(tenant_id, user_id):
    """A transaction above CTR threshold — should trigger HIGH risk."""
    txn = MagicMock(spec=Transaction)
    txn.id = uuid.uuid4()
    txn.tenant_id = tenant_id
    txn.amount = Decimal("15000.00")
    txn.currency = "USD"
    txn.initiated_by = user_id
    txn.status = TransactionStatus.COMPLETED
    txn.created_at = MagicMock()
    return txn


@pytest.fixture
def structuring_transaction(tenant_id, user_id):
    """A transaction just below CTR threshold — possible structuring."""
    txn = MagicMock(spec=Transaction)
    txn.id = uuid.uuid4()
    txn.tenant_id = tenant_id
    txn.amount = Decimal("9500.00")
    txn.currency = "USD"
    txn.initiated_by = user_id
    txn.status = TransactionStatus.COMPLETED
    txn.created_at = MagicMock()
    return txn


def _mock_db(velocity_count=0, daily_total=Decimal("0")):
    """Create a mock db session with configurable query results."""
    db = AsyncMock()

    # Velocity query result
    velocity_result = MagicMock()
    velocity_result.scalar = MagicMock(return_value=velocity_count)

    # Daily aggregate query result
    daily_result = MagicMock()
    daily_result.scalar = MagicMock(return_value=daily_total)

    db.execute = AsyncMock(side_effect=[velocity_result, daily_result])
    db.add = MagicMock()
    db.commit = AsyncMock()

    return db


class TestComplianceScreening:
    """Test AML/CTR/SAR transaction screening rules."""

    @pytest.mark.asyncio
    async def test_small_transaction_low_risk(self, tenant_id, small_transaction):
        """Normal small transaction passes with LOW risk."""
        db = _mock_db(velocity_count=1, daily_total=Decimal("100.00"))

        risk = await screen_transaction(db, tenant_id=tenant_id, transaction=small_transaction)

        assert risk == RiskLevel.LOW

    @pytest.mark.asyncio
    async def test_large_transaction_triggers_ctr(self, tenant_id, large_transaction):
        """Transaction > $10,000 triggers CTR (HIGH+ risk)."""
        db = _mock_db(velocity_count=1, daily_total=Decimal("0"))

        risk = await screen_transaction(db, tenant_id=tenant_id, transaction=large_transaction)

        assert risk in (RiskLevel.HIGH, RiskLevel.CRITICAL)

    @pytest.mark.asyncio
    async def test_structuring_detection(self, tenant_id, structuring_transaction):
        """Transaction between $9,000-$10,000 triggers structuring alert."""
        db = _mock_db(velocity_count=1, daily_total=Decimal("0"))

        risk = await screen_transaction(db, tenant_id=tenant_id, transaction=structuring_transaction)

        assert risk in (RiskLevel.MEDIUM, RiskLevel.HIGH)

    @pytest.mark.asyncio
    async def test_high_velocity_triggers_sar(self, tenant_id, small_transaction):
        """Too many transactions per hour triggers SAR review."""
        db = _mock_db(velocity_count=SAR_VELOCITY_THRESHOLD + 1, daily_total=Decimal("200.00"))

        risk = await screen_transaction(db, tenant_id=tenant_id, transaction=small_transaction)

        assert risk in (RiskLevel.MEDIUM, RiskLevel.HIGH)

    @pytest.mark.asyncio
    async def test_daily_aggregate_exceeded(self, tenant_id, small_transaction):
        """Daily total exceeding threshold triggers alert."""
        db = _mock_db(
            velocity_count=2,
            daily_total=DAILY_AGGREGATE_THRESHOLD_USD - Decimal("10.00"),
        )

        risk = await screen_transaction(db, tenant_id=tenant_id, transaction=small_transaction)

        assert risk in (RiskLevel.MEDIUM, RiskLevel.HIGH)

    @pytest.mark.asyncio
    async def test_combined_risk_factors_critical(self, tenant_id, large_transaction):
        """Multiple risk factors together escalate to CRITICAL."""
        db = _mock_db(
            velocity_count=SAR_VELOCITY_THRESHOLD + 2,
            daily_total=Decimal("20000.00"),
        )

        risk = await screen_transaction(db, tenant_id=tenant_id, transaction=large_transaction)

        assert risk == RiskLevel.CRITICAL

    @pytest.mark.asyncio
    async def test_compliance_record_created_for_nontrivial_risk(self, tenant_id, large_transaction):
        """Non-LOW risk creates a ComplianceRecord in the database."""
        db = _mock_db(velocity_count=1, daily_total=Decimal("0"))

        await screen_transaction(db, tenant_id=tenant_id, transaction=large_transaction)

        # db.add should have been called with a ComplianceRecord
        assert db.add.called
        assert db.commit.called
