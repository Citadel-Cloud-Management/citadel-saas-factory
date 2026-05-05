"""Tests for the double-entry ledger service — critical financial path."""

import uuid
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.account import Account, AccountStatus, AccountType
from app.models.transaction import TransactionStatus, TransactionType
from app.services.ledger import (
    AccountNotActiveError,
    DuplicateTransactionError,
    InsufficientFundsError,
    execute_transfer,
)


@pytest.fixture
def tenant_id():
    return uuid.uuid4()


@pytest.fixture
def user_id():
    return uuid.uuid4()


@pytest.fixture
def active_account(tenant_id, user_id):
    """Create a mock active account with balance."""
    account = MagicMock(spec=Account)
    account.id = uuid.uuid4()
    account.tenant_id = tenant_id
    account.user_id = user_id
    account.status = AccountStatus.ACTIVE
    account.balance = Decimal("1000.00")
    account.available_balance = Decimal("1000.00")
    account.currency = "USD"
    return account


@pytest.fixture
def frozen_account(tenant_id, user_id):
    """Create a mock frozen account."""
    account = MagicMock(spec=Account)
    account.id = uuid.uuid4()
    account.tenant_id = tenant_id
    account.status = AccountStatus.FROZEN
    account.balance = Decimal("500.00")
    account.available_balance = Decimal("500.00")
    return account


class TestExecuteTransfer:
    """Test the core transfer operation."""

    @pytest.mark.asyncio
    async def test_successful_transfer(self, tenant_id, user_id, active_account):
        """Transfer between two active accounts with sufficient funds."""
        credit_account = MagicMock(spec=Account)
        credit_account.id = uuid.uuid4()
        credit_account.status = AccountStatus.ACTIVE
        credit_account.balance = Decimal("200.00")
        credit_account.available_balance = Decimal("200.00")

        db = AsyncMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=None)))
        db.get = AsyncMock(side_effect=[active_account, credit_account])
        db.add = MagicMock()
        db.commit = AsyncMock()
        db.refresh = AsyncMock()

        result = await execute_transfer(
            db,
            tenant_id=tenant_id,
            debit_account_id=active_account.id,
            credit_account_id=credit_account.id,
            amount=Decimal("100.00"),
            currency="USD",
            transaction_type=TransactionType.TRANSFER,
            initiated_by=user_id,
            idempotency_key="test-key-001",
        )

        # Verify balances updated
        assert active_account.balance == Decimal("900.00")
        assert credit_account.balance == Decimal("300.00")
        assert db.commit.called

    @pytest.mark.asyncio
    async def test_insufficient_funds_rejected(self, tenant_id, user_id, active_account):
        """Transfer exceeding available balance is rejected."""
        credit_account = MagicMock(spec=Account)
        credit_account.id = uuid.uuid4()
        credit_account.status = AccountStatus.ACTIVE

        db = AsyncMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=None)))
        db.get = AsyncMock(side_effect=[active_account, credit_account])

        with pytest.raises(InsufficientFundsError):
            await execute_transfer(
                db,
                tenant_id=tenant_id,
                debit_account_id=active_account.id,
                credit_account_id=credit_account.id,
                amount=Decimal("2000.00"),  # More than available
                currency="USD",
                transaction_type=TransactionType.TRANSFER,
                initiated_by=user_id,
                idempotency_key="test-key-002",
            )

    @pytest.mark.asyncio
    async def test_frozen_account_rejected(self, tenant_id, user_id, frozen_account):
        """Transfer from/to frozen account is rejected."""
        credit_account = MagicMock(spec=Account)
        credit_account.id = uuid.uuid4()
        credit_account.status = AccountStatus.ACTIVE

        db = AsyncMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=None)))
        db.get = AsyncMock(side_effect=[frozen_account, credit_account])

        with pytest.raises(AccountNotActiveError):
            await execute_transfer(
                db,
                tenant_id=tenant_id,
                debit_account_id=frozen_account.id,
                credit_account_id=credit_account.id,
                amount=Decimal("50.00"),
                currency="USD",
                transaction_type=TransactionType.TRANSFER,
                initiated_by=user_id,
                idempotency_key="test-key-003",
            )

    @pytest.mark.asyncio
    async def test_idempotency_returns_existing(self, tenant_id, user_id):
        """Duplicate idempotency_key returns existing transaction."""
        existing_txn = MagicMock()
        existing_txn.reference_id = "TXN-EXISTING"

        db = AsyncMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=existing_txn)))

        with pytest.raises(DuplicateTransactionError) as exc_info:
            await execute_transfer(
                db,
                tenant_id=tenant_id,
                debit_account_id=uuid.uuid4(),
                credit_account_id=uuid.uuid4(),
                amount=Decimal("100.00"),
                currency="USD",
                transaction_type=TransactionType.TRANSFER,
                initiated_by=user_id,
                idempotency_key="duplicate-key",
            )

        assert exc_info.value.transaction == existing_txn

    @pytest.mark.asyncio
    async def test_double_entry_creates_two_ledger_entries(self, tenant_id, user_id, active_account):
        """Every transfer creates exactly 2 ledger entries (debit + credit)."""
        credit_account = MagicMock(spec=Account)
        credit_account.id = uuid.uuid4()
        credit_account.status = AccountStatus.ACTIVE
        credit_account.balance = Decimal("0.00")
        credit_account.available_balance = Decimal("0.00")

        db = AsyncMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=None)))
        db.get = AsyncMock(side_effect=[active_account, credit_account])
        added_objects = []
        db.add = MagicMock(side_effect=lambda obj: added_objects.append(obj))
        db.commit = AsyncMock()
        db.refresh = AsyncMock()

        await execute_transfer(
            db,
            tenant_id=tenant_id,
            debit_account_id=active_account.id,
            credit_account_id=credit_account.id,
            amount=Decimal("250.00"),
            currency="USD",
            transaction_type=TransactionType.TRANSFER,
            initiated_by=user_id,
            idempotency_key="test-key-004",
        )

        # 1 Transaction + 2 LedgerEntries = 3 objects added
        assert len(added_objects) == 3
