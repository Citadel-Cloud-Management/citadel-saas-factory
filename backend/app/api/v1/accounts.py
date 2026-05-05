"""Accounts API — financial account management for tenants."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account, AccountStatus, AccountType

router = APIRouter(prefix="/accounts", tags=["accounts"])


# ─── Schemas ────────────────────────────────────────────────────────────


class CreateAccountRequest(BaseModel):
    account_type: AccountType
    currency: str = Field(default="USD", max_length=3, min_length=3)


class AccountResponse(BaseModel):
    id: str
    account_type: str
    currency: str
    balance: str
    available_balance: str
    status: str
    account_number: str
    created_at: str

    class Config:
        from_attributes = True


# ─── Endpoints ──────────────────────────────────────────────────────────


@router.get("", response_model=list[AccountResponse])
async def list_accounts(request: Request) -> list[AccountResponse]:
    """List all accounts for the authenticated user's tenant."""
    tenant_id = _require_tenant(request)
    db: AsyncSession = request.state.db

    result = await db.execute(
        select(Account)
        .where(Account.tenant_id == tenant_id)
        .order_by(Account.created_at.desc())
    )
    accounts = result.scalars().all()

    return [_to_response(a) for a in accounts]


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(account_id: str, request: Request) -> AccountResponse:
    """Get a specific account by ID."""
    tenant_id = _require_tenant(request)
    db: AsyncSession = request.state.db

    account = await _get_account_or_404(db, account_id, tenant_id)
    return _to_response(account)


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(request: Request, body: CreateAccountRequest) -> AccountResponse:
    """Create a new financial account."""
    tenant_id = _require_tenant(request)
    user_id = _require_user(request)
    db: AsyncSession = request.state.db

    account_number = f"CIT-{uuid.uuid4().hex[:12].upper()}"

    account = Account(
        tenant_id=tenant_id,
        user_id=user_id,
        account_type=body.account_type,
        currency=body.currency.upper(),
        balance=0,
        available_balance=0,
        status=AccountStatus.ACTIVE,
        account_number=account_number,
    )
    db.add(account)
    await db.commit()
    await db.refresh(account)

    return _to_response(account)


@router.post("/{account_id}/freeze", response_model=AccountResponse)
async def freeze_account(account_id: str, request: Request) -> AccountResponse:
    """Freeze an account (compliance or fraud hold). Requires admin/compliance role."""
    tenant_id = _require_tenant(request)
    _require_role(request, "admin", "compliance_officer", "owner")
    db: AsyncSession = request.state.db

    account = await _get_account_or_404(db, account_id, tenant_id)

    if account.status == AccountStatus.CLOSED:
        raise HTTPException(status_code=400, detail="Cannot freeze a closed account")

    account.status = AccountStatus.FROZEN
    await db.commit()
    await db.refresh(account)

    return _to_response(account)


@router.post("/{account_id}/unfreeze", response_model=AccountResponse)
async def unfreeze_account(account_id: str, request: Request) -> AccountResponse:
    """Unfreeze a frozen account. Requires admin/compliance role."""
    tenant_id = _require_tenant(request)
    _require_role(request, "admin", "compliance_officer", "owner")
    db: AsyncSession = request.state.db

    account = await _get_account_or_404(db, account_id, tenant_id)

    if account.status != AccountStatus.FROZEN:
        raise HTTPException(status_code=400, detail="Account is not frozen")

    account.status = AccountStatus.ACTIVE
    await db.commit()
    await db.refresh(account)

    return _to_response(account)


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


def _require_role(request: Request, *allowed_roles: str) -> None:
    """Verify the authenticated user has one of the allowed roles."""
    user_role = getattr(request.state, "user_role", None)
    if user_role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")


async def _get_account_or_404(db: AsyncSession, account_id: str, tenant_id: uuid.UUID) -> Account:
    result = await db.execute(
        select(Account)
        .where(Account.id == account_id)
        .where(Account.tenant_id == tenant_id)
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


def _to_response(account: Account) -> AccountResponse:
    return AccountResponse(
        id=str(account.id),
        account_type=account.account_type,
        currency=account.currency,
        balance=str(account.balance),
        available_balance=str(account.available_balance),
        status=account.status,
        account_number=account.account_number,
        created_at=account.created_at.isoformat(),
    )
