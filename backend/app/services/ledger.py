"""Ledger service — double-entry accounting with idempotency guarantees.

Every financial transaction creates exactly two ledger entries:
- One DEBIT entry (reduces source account balance)
- One CREDIT entry (increases destination account balance)

Idempotency: duplicate requests with the same idempotency_key return the
existing transaction without creating a new one.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account, AccountStatus
from app.models.ledger_entry import EntryType, LedgerEntry
from app.models.transaction import Transaction, TransactionStatus, TransactionType


class InsufficientFundsError(Exception):
    """Raised when debit account has insufficient available balance."""


class AccountNotActiveError(Exception):
    """Raised when an account is not in active status."""


class DuplicateTransactionError(Exception):
    """Raised when idempotency_key already exists (returns existing transaction)."""

    def __init__(self, existing_transaction: Transaction) -> None:
        self.transaction = existing_transaction
        super().__init__(f"Duplicate transaction: {existing_transaction.reference_id}")


async def execute_transfer(
    db: AsyncSession,
    *,
    tenant_id: uuid.UUID,
    debit_account_id: uuid.UUID,
    credit_account_id: uuid.UUID,
    amount: Decimal,
    currency: str,
    transaction_type: TransactionType,
    initiated_by: uuid.UUID,
    idempotency_key: str,
    description: str | None = None,
    metadata: dict | None = None,
) -> Transaction:
    """Execute a double-entry transfer between two accounts.

    This is the core financial operation. It:
    1. Checks idempotency (returns existing if duplicate)
    2. Validates both accounts are active
    3. Checks sufficient funds in debit account
    4. Creates the Transaction record
    5. Creates two LedgerEntry records (debit + credit)
    6. Updates account balances atomically

    All within a single database transaction for ACID guarantees.
    """
    # 1. Idempotency check (tenant-scoped to prevent cross-tenant collisions)
    existing = await db.execute(
        select(Transaction)
        .where(Transaction.idempotency_key == idempotency_key)
        .where(Transaction.tenant_id == tenant_id)
    )
    if found := existing.scalar_one_or_none():
        raise DuplicateTransactionError(found)

    # 2. Load and validate accounts (SELECT FOR UPDATE with consistent lock ordering)
    # Lock in sorted UUID order to prevent deadlocks on A→B / B→A concurrent transfers
    ordered_ids = sorted([debit_account_id, credit_account_id])
    result = await db.execute(
        select(Account)
        .where(Account.id.in_(ordered_ids))
        .order_by(Account.id)
        .with_for_update()
    )
    locked_accounts = {a.id: a for a in result.scalars().all()}
    debit_account = locked_accounts.get(debit_account_id)
    credit_account = locked_accounts.get(credit_account_id)

    if not debit_account or debit_account.status != AccountStatus.ACTIVE:
        raise AccountNotActiveError(f"Debit account {debit_account_id} is not active")
    if not credit_account or credit_account.status != AccountStatus.ACTIVE:
        raise AccountNotActiveError(f"Credit account {credit_account_id} is not active")

    # 3. Sufficient funds check
    if debit_account.available_balance < amount:
        raise InsufficientFundsError(
            f"Account {debit_account_id} has {debit_account.available_balance} "
            f"available but {amount} required"
        )

    # 4. Create transaction
    reference_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    transaction = Transaction(
        tenant_id=tenant_id,
        reference_id=reference_id,
        idempotency_key=idempotency_key,
        debit_account_id=debit_account_id,
        credit_account_id=credit_account_id,
        amount=amount,
        currency=currency,
        transaction_type=transaction_type,
        status=TransactionStatus.COMPLETED,
        description=description,
        extra_data=metadata,
        initiated_by=initiated_by,
        completed_at=datetime.now(timezone.utc),
    )
    db.add(transaction)

    # 5. Create ledger entries
    new_debit_balance = debit_account.balance - amount
    new_credit_balance = credit_account.balance + amount

    debit_entry = LedgerEntry(
        tenant_id=tenant_id,
        transaction_id=transaction.id,
        account_id=debit_account_id,
        entry_type=EntryType.DEBIT,
        amount=amount,
        currency=currency,
        running_balance=new_debit_balance,
    )
    credit_entry = LedgerEntry(
        tenant_id=tenant_id,
        transaction_id=transaction.id,
        account_id=credit_account_id,
        entry_type=EntryType.CREDIT,
        amount=amount,
        currency=currency,
        running_balance=new_credit_balance,
    )
    db.add(debit_entry)
    db.add(credit_entry)

    # 6. Update account balances
    debit_account.balance = new_debit_balance
    debit_account.available_balance = new_debit_balance
    credit_account.balance = new_credit_balance
    credit_account.available_balance = new_credit_balance

    await db.commit()
    await db.refresh(transaction)

    return transaction
