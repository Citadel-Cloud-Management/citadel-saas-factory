"""Transaction model — financial transactions with idempotency and double-entry."""

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin


class TransactionType(str, enum.Enum):
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    PAYMENT = "payment"
    REFUND = "refund"
    FEE = "fee"
    REMITTANCE = "remittance"


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"
    CANCELLED = "cancelled"


class Transaction(TenantMixin, Base):
    """A financial transaction between accounts with idempotency guarantees."""

    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    debit_account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), index=True, nullable=False)
    credit_account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), index=True, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(String(32), nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(String(32), nullable=False, default=TransactionStatus.PENDING)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_data: Mapped[dict | None] = mapped_column("extra_data", JSONB, nullable=True)
    initiated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<Transaction {self.reference_id} {self.amount} {self.currency} {self.status}>"
