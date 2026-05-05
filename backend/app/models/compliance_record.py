"""Compliance record model — regulatory events, AML screening, suspicious activity."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin


class ComplianceEventType(str, enum.Enum):
    KYC_CHECK = "kyc_check"
    AML_SCREEN = "aml_screen"
    TRANSACTION_REVIEW = "transaction_review"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    REGULATORY_REPORT = "regulatory_report"
    SANCTIONS_CHECK = "sanctions_check"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceRecord(TenantMixin, Base):
    """Audit and compliance event record for regulatory requirements."""

    __tablename__ = "compliance_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type: Mapped[ComplianceEventType] = mapped_column(String(32), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="user, transaction, account")
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    risk_level: Mapped[RiskLevel] = mapped_column(String(16), nullable=False, default=RiskLevel.LOW)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resolution: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<ComplianceRecord {self.event_type} risk={self.risk_level} entity={self.entity_type}:{self.entity_id}>"
