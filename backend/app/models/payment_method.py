"""Payment method model — linked bank accounts, cards, crypto wallets."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin


class PaymentMethodType(str, enum.Enum):
    BANK_ACCOUNT = "bank_account"
    CARD = "card"
    CRYPTO_WALLET = "crypto_wallet"
    MOBILE_MONEY = "mobile_money"


class PaymentMethod(TenantMixin, Base):
    """A linked payment method for deposits and withdrawals."""

    __tablename__ = "payment_methods"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    method_type: Mapped[PaymentMethodType] = mapped_column(String(32), nullable=False)
    provider: Mapped[str] = mapped_column(String(32), nullable=False, comment="stripe, plaid, wise")
    provider_reference_id: Mapped[str] = mapped_column(String(128), nullable=False)
    last_four: Mapped[str | None] = mapped_column(String(4), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    extra_data: Mapped[dict | None] = mapped_column("extra_data", JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<PaymentMethod {self.method_type} ****{self.last_four} verified={self.is_verified}>"
