# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Email: security@citadelcloudmanagement.com

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Security Practices

This project enforces:

- No hardcoded secrets (environment variables or HashiCorp Vault)
- Parameterized queries only (no SQL string concatenation)
- Rate limiting on all API endpoints
- CORS, CSRF, XSS protection on all routes
- Container image scanning (Trivy) before deployment
- Secret scanning in pre-commit hooks (TruffleHog)
- Runtime threat detection (Falco)
- Kubernetes admission policies (Kyverno)
- LLM output validation through triple-layer guardrails

## Supported Versions

| Version | Supported |
|---------|-----------|
| 3.x     | Yes       |
| < 3.0   | No        |
