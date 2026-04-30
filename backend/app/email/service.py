"""Email service — high-level helpers for transactional emails."""

from __future__ import annotations

from app.email.client import EmailClient, EmailConfig


class EmailService:
    """Facade over EmailClient for common transactional emails."""

    def __init__(self, client: EmailClient | None = None) -> None:
        self._client = client or EmailClient(EmailConfig())

    async def send_welcome_email(
        self,
        user_email: str,
        user_name: str,
        login_url: str,
    ) -> None:
        """Send a welcome email after registration."""
        await self._client.send_template(
            to=user_email,
            template_name="welcome",
            context={"name": user_name, "login_url": login_url},
        )

    async def send_password_reset_email(
        self,
        user_email: str,
        user_name: str,
        reset_url: str,
        expires_in: str = "1 hour",
    ) -> None:
        """Send a password-reset email with a time-limited link."""
        await self._client.send_template(
            to=user_email,
            template_name="password_reset",
            context={
                "name": user_name,
                "reset_url": reset_url,
                "expires_in": expires_in,
            },
        )

    async def send_invoice_email(
        self,
        user_email: str,
        user_name: str,
        amount: str,
        plan: str,
        date: str,
    ) -> None:
        """Send an invoice/receipt email after payment."""
        await self._client.send_template(
            to=user_email,
            template_name="invoice_receipt",
            context={
                "name": user_name,
                "amount": amount,
                "plan": plan,
                "date": date,
            },
        )

    async def send_tenant_invite(
        self,
        user_email: str,
        inviter_name: str,
        tenant_name: str,
        invite_url: str,
    ) -> None:
        """Send an invitation to join a tenant/workspace."""
        await self._client.send_template(
            to=user_email,
            template_name="tenant_invite",
            context={
                "inviter_name": inviter_name,
                "tenant_name": tenant_name,
                "invite_url": invite_url,
            },
        )
