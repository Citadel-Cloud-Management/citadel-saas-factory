"""Email client — async SMTP transport via aiosmtplib."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
import structlog

from app.email.templates import TEMPLATES

logger = structlog.get_logger(__name__)


@dataclass(frozen=True)
class EmailConfig:
    """Immutable SMTP configuration loaded from environment variables."""

    host: str = field(default_factory=lambda: os.getenv("SMTP_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", "1025")))
    user: str = field(default_factory=lambda: os.getenv("SMTP_USER", ""))
    password: str = field(default_factory=lambda: os.getenv("SMTP_PASSWORD", ""))
    use_tls: bool = field(
        default_factory=lambda: os.getenv("SMTP_USE_TLS", "false").lower() == "true",
    )
    email_from: str = field(
        default_factory=lambda: os.getenv("EMAIL_FROM", "noreply@citadel.local"),
    )


class EmailClient:
    """Sends emails asynchronously via aiosmtplib."""

    def __init__(self, config: EmailConfig | None = None) -> None:
        self._config = config or EmailConfig()

    async def send_email(
        self,
        to: str,
        subject: str,
        html_body: str,
        text_body: str | None = None,
    ) -> None:
        """Send an email with HTML (and optional plaintext) body."""
        msg = MIMEMultipart("alternative")
        msg["From"] = self._config.email_from
        msg["To"] = to
        msg["Subject"] = subject

        if text_body is not None:
            msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            await aiosmtplib.send(
                msg,
                hostname=self._config.host,
                port=self._config.port,
                username=self._config.user or None,
                password=self._config.password or None,
                use_tls=self._config.use_tls,
            )
            logger.info(
                "email_sent",
                to=to,
                subject=subject,
                smtp_host=self._config.host,
            )
        except aiosmtplib.SMTPException:
            logger.exception(
                "email_send_failed",
                to=to,
                subject=subject,
                smtp_host=self._config.host,
            )
            raise

    async def send_template(
        self,
        to: str,
        template_name: str,
        context: dict[str, str],
    ) -> None:
        """Render a named template with *context* and send it."""
        template = TEMPLATES.get(template_name)
        if template is None:
            msg = f"Unknown email template: {template_name}"
            raise ValueError(msg)

        subject = template["subject"].safe_substitute(context)
        html_body = template["html_body"].safe_substitute(context)
        text_body_tmpl = template.get("text_body")
        text_body = text_body_tmpl.safe_substitute(context) if text_body_tmpl else None

        await self.send_email(to=to, subject=subject, html_body=html_body, text_body=text_body)
