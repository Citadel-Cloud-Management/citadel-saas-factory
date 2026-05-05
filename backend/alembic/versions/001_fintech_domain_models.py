"""Fintech domain models — accounts, transactions, ledger, KYC, payments, compliance.

Revision ID: 001_fintech
Revises:
Create Date: 2026-05-05
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001_fintech"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Accounts
    op.create_table(
        "accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("account_type", sa.String(32), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False, server_default="USD"),
        sa.Column("balance", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("available_balance", sa.Numeric(18, 4), nullable=False, server_default="0"),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending_verification"),
        sa.Column("account_number", sa.String(34), unique=True, nullable=False, index=True),
        sa.Column("routing_number", sa.String(12), nullable=True),
        sa.Column("institution_name", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Transactions
    op.create_table(
        "transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("reference_id", sa.String(64), unique=True, nullable=False, index=True),
        sa.Column("idempotency_key", sa.String(128), unique=True, nullable=False, index=True),
        sa.Column("debit_account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("accounts.id"), nullable=False, index=True),
        sa.Column("credit_account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("accounts.id"), nullable=False, index=True),
        sa.Column("amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("transaction_type", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("metadata", postgresql.JSONB, nullable=True),
        sa.Column("initiated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Ledger Entries (immutable)
    op.create_table(
        "ledger_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("transaction_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("transactions.id"), nullable=False, index=True),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("accounts.id"), nullable=False, index=True),
        sa.Column("entry_type", sa.String(8), nullable=False),
        sa.Column("amount", sa.Numeric(18, 4), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("running_balance", sa.Numeric(18, 4), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        comment="Immutable double-entry ledger - never update or delete rows",
    )

    # KYC Records
    op.create_table(
        "kyc_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("verification_level", sa.String(16), nullable=False, server_default="none"),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("provider_reference_id", sa.String(128), nullable=True),
        sa.Column("document_type", sa.String(32), nullable=True),
        sa.Column("risk_score", sa.Integer, nullable=False, server_default="0"),
        sa.Column("rejection_reason", sa.Text, nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Payment Methods
    op.create_table(
        "payment_methods",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("method_type", sa.String(32), nullable=False),
        sa.Column("provider", sa.String(32), nullable=False),
        sa.Column("provider_reference_id", sa.String(128), nullable=False),
        sa.Column("last_four", sa.String(4), nullable=True),
        sa.Column("is_default", sa.Boolean, server_default="false", nullable=False),
        sa.Column("is_verified", sa.Boolean, server_default="false", nullable=False),
        sa.Column("metadata", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Compliance Records
    op.create_table(
        "compliance_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("event_type", sa.String(32), nullable=False),
        sa.Column("entity_type", sa.String(64), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column("risk_level", sa.String(16), nullable=False, server_default="low"),
        sa.Column("details", postgresql.JSONB, nullable=True),
        sa.Column("reviewer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("resolution", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Row-level security policies (for multi-tenant isolation)
    op.execute("ALTER TABLE accounts ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE transactions ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE ledger_entries ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE kyc_records ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE payment_methods ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE compliance_records ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    op.drop_table("compliance_records")
    op.drop_table("payment_methods")
    op.drop_table("kyc_records")
    op.drop_table("ledger_entries")
    op.drop_table("transactions")
    op.drop_table("accounts")
