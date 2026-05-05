"""Financial account model — multi-currency accounts with tenant isolation."""

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin


class AccountType(str, enum.Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    WALLET = "wallet"
    ESCROW = "escrow"


class AccountStatus(str, enum.Enum):
    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"
    PENDING_VERIFICATION = "pending_verification"


class Account(TenantMixin, Base):
    """A financial account belonging to a user within a tenant."""

    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    account_type: Mapped[AccountType] = mapped_column(String(32), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False, default=0)
    available_balance: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False, default=0)
    status: Mapped[AccountStatus] = mapped_column(String(32), nullable=False, default=AccountStatus.PENDING_VERIFICATION)
    account_number: Mapped[str] = mapped_column(String(34), unique=True, index=True, nullable=False)
    routing_number: Mapped[str | None] = mapped_column(String(12), nullable=True)
    institution_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Account {self.account_number} type={self.account_type} balance={self.balance}>"
