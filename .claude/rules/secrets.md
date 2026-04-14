# Secrets Management Rules
- Production: HashiCorp Vault only
- Development: environment variables via .env (never committed)
- Rotation policy: every 90 days
- Pre-commit scanning with TruffleHog
- No secrets in CI/CD logs — mask all sensitive values
- GitHub Secrets for Actions workflows
