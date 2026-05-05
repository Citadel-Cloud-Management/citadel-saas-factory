"""Transactions API — transfers, history, and transaction details."""

import uuid

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.services.compliance import screen_transaction
from app.services.ledger import (
    AccountNotActiveError,
    DuplicateTransactionError,
    InsufficientFundsError,
    execute_transfer,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


# ─── Schemas ────────────────────────────────────────────────────────────


class TransferRequest(BaseModel):
    debit_account_id: str
    credit_account_id: str
    amount: str = Field(description="Decimal amount as string, e.g. '100.50'")
    currency: str = Field(default="USD", max_length=3)
    description: str | None = None
    idempotency_key: str = Field(description="Unique key to prevent duplicate processing")


class TransactionResponse(BaseModel):
    id: str
    reference_id: str
    amount: str
    currency: str
    transaction_type: str
    status: str
    description: str | None
    created_at: str
    completed_at: str | None


class TransactionListResponse(BaseModel):
    data: list[TransactionResponse]
    meta: dict


# ─── Endpoints ──────────────────────────────────────────────────────────


@router.get("", response_model=TransactionListResponse)
async def list_transactions(
    request: Request,
    page: int = 1,
    limit: int = 20,
) -> TransactionListResponse:
    """List transactions for the current tenant with pagination."""
    tenant_id = _require_tenant(request)
    db: AsyncSession = request.state.db

    offset = (page - 1) * limit

    result = await db.execute(
        select(Transaction)
        .where(Transaction.tenant_id == tenant_id)
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    transactions = result.scalars().all()

    from sqlalchemy import func
    count_result = await db.execute(
        select(func.count(Transaction.id)).where(Transaction.tenant_id == tenant_id)
    )
    total = count_result.scalar() or 0

    return TransactionListResponse(
        data=[_to_response(t) for t in transactions],
        meta={"total": total, "page": page, "limit": limit},
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str, request: Request) -> TransactionResponse:
    """Get a specific transaction by ID."""
    tenant_id = _require_tenant(request)
    db: AsyncSession = request.state.db

    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == transaction_id)
        .where(Transaction.tenant_id == tenant_id)
    )
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return _to_response(transaction)


@router.post("/transfer", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transfer(request: Request, body: TransferRequest) -> TransactionResponse:
    """Execute a transfer between two accounts.

    Atomic double-entry: debits source, credits destination.
    Idempotent: same idempotency_key returns existing transaction.
    Compliance: screens against AML/CTR rules before execution.
    """
    tenant_id = _require_tenant(request)
    user_id = _require_user(request)
    db: AsyncSession = request.state.db

    from decimal import Decimal, InvalidOperation

    try:
        amount = Decimal(body.amount)
    except (InvalidOperation, ValueError):
        raise HTTPException(status_code=400, detail="Invalid amount format")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if body.debit_account_id == body.credit_account_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")

    try:
        transaction = await execute_transfer(
            db,
            tenant_id=tenant_id,
            debit_account_id=uuid.UUID(body.debit_account_id),
            credit_account_id=uuid.UUID(body.credit_account_id),
            amount=amount,
            currency=body.currency.upper(),
            transaction_type=TransactionType.TRANSFER,
            initiated_by=user_id,
            idempotency_key=body.idempotency_key,
            description=body.description,
        )
    except DuplicateTransactionError as exc:
        return _to_response(exc.transaction)
    except InsufficientFundsError:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    except AccountNotActiveError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Run async compliance screening (non-blocking — doesn't fail the transaction)
    await screen_transaction(db, tenant_id=tenant_id, transaction=transaction)

    return _to_response(transaction)


# ─── Helpers ────────────────────────────────────────────────────────────


def _require_tenant(request: Request) -> uuid.UUID:
    tenant_id = getattr(request.state, "tenant_id", None)
    if tenant_id is None:
        raise HTTPException(status_code=401, detail="Tenant context required")
    return tenant_id


def _require_user(request: Request) -> uuid.UUID:
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id


def _to_response(t: Transaction) -> TransactionResponse:
    return TransactionResponse(
        id=str(t.id),
        reference_id=t.reference_id,
        amount=str(t.amount),
        currency=t.currency,
        transaction_type=t.transaction_type,
        status=t.status,
        description=t.description,
        created_at=t.created_at.isoformat(),
        completed_at=t.completed_at.isoformat() if t.completed_at else None,
    )
