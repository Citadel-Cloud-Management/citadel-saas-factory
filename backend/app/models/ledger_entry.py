"""Ledger entry model — immutable double-entry accounting records."""

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin


class EntryType(str, enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class LedgerEntry(TenantMixin, Base):
    """Immutable double-entry ledger record. Never update or delete rows."""

    __tablename__ = "ledger_entries"
    __table_args__ = ({"comment": "Immutable double-entry ledger - never update or delete rows"},)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("transactions.id"), index=True, nullable=False)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("accounts.id"), index=True, nullable=False)
    entry_type: Mapped[EntryType] = mapped_column(String(8), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    running_balance: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<LedgerEntry {self.entry_type} {self.amount} {self.currency} acct={self.account_id}>"
