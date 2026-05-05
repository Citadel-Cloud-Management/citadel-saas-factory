"""KYC verification model — identity verification and AML compliance."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin


class VerificationLevel(str, enum.Enum):
    NONE = "none"
    BASIC = "basic"
    ENHANCED = "enhanced"
    FULL = "full"


class KYCStatus(str, enum.Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class DocumentType(str, enum.Enum):
    PASSPORT = "passport"
    DRIVERS_LICENSE = "drivers_license"
    NATIONAL_ID = "national_id"
    UTILITY_BILL = "utility_bill"
    BANK_STATEMENT = "bank_statement"


class KYCRecord(TenantMixin, Base):
    """KYC/AML verification record for a user."""

    __tablename__ = "kyc_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)
    verification_level: Mapped[VerificationLevel] = mapped_column(String(16), nullable=False, default=VerificationLevel.NONE)
    status: Mapped[KYCStatus] = mapped_column(String(16), nullable=False, default=KYCStatus.PENDING)
    provider: Mapped[str] = mapped_column(String(32), nullable=False, comment="sumsub, onfido, manual")
    provider_reference_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    document_type: Mapped[DocumentType | None] = mapped_column(String(32), nullable=True)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="0-100 scale")
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<KYCRecord user={self.user_id} level={self.verification_level} status={self.status}>"
