"""Email templates — Python string.Template definitions for transactional emails."""

from __future__ import annotations

from string import Template

# ---------------------------------------------------------------------------
# Welcome email — sent after user registration
# ---------------------------------------------------------------------------
WELCOME_EMAIL = {
    "subject": Template("Welcome to Citadel, $name!"),
    "html_body": Template(
        "<html><body>"
        "<h1>Welcome, $name!</h1>"
        "<p>Your account has been created successfully.</p>"
        '<p><a href="$login_url">Log in to your dashboard</a></p>'
        "<p>— The Citadel Team</p>"
        "</body></html>"
    ),
}

# ---------------------------------------------------------------------------
# Password reset — contains a time-limited reset link
# ---------------------------------------------------------------------------
PASSWORD_RESET = {
    "subject": Template("Password Reset Request"),
    "html_body": Template(
        "<html><body>"
        "<h1>Password Reset</h1>"
        "<p>Hi $name,</p>"
        "<p>We received a request to reset your password.</p>"
        '<p><a href="$reset_url">Reset your password</a></p>'
        "<p>This link expires in $expires_in.</p>"
        "<p>If you did not request this, please ignore this email.</p>"
        "<p>— The Citadel Team</p>"
        "</body></html>"
    ),
}

# ---------------------------------------------------------------------------
# Invoice receipt — sent after a successful payment
# ---------------------------------------------------------------------------
INVOICE_RECEIPT = {
    "subject": Template("Payment Received — $amount"),
    "html_body": Template(
        "<html><body>"
        "<h1>Payment Confirmation</h1>"
        "<p>Hi $name,</p>"
        "<p>We received your payment of <strong>$amount</strong> "
        "for the <strong>$plan</strong> plan on $date.</p>"
        "<p>Thank you for your business!</p>"
        "<p>— The Citadel Team</p>"
        "</body></html>"
    ),
}

# ---------------------------------------------------------------------------
# Tenant invite — invite a user to join a tenant / workspace
# ---------------------------------------------------------------------------
TENANT_INVITE = {
    "subject": Template("$inviter_name invited you to $tenant_name"),
    "html_body": Template(
        "<html><body>"
        "<h1>You have been invited!</h1>"
        "<p><strong>$inviter_name</strong> has invited you to join "
        "<strong>$tenant_name</strong> on Citadel.</p>"
        '<p><a href="$invite_url">Accept Invitation</a></p>'
        "<p>— The Citadel Team</p>"
        "</body></html>"
    ),
}

# ---------------------------------------------------------------------------
# Registry — maps template names to their definitions
# ---------------------------------------------------------------------------
TEMPLATES: dict[str, dict[str, Template]] = {
    "welcome": WELCOME_EMAIL,
    "password_reset": PASSWORD_RESET,
    "invoice_receipt": INVOICE_RECEIPT,
    "tenant_invite": TENANT_INVITE,
}
