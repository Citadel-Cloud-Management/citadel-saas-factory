# Security Rules
- No hardcoded secrets — use environment variables or Vault
- Validate all user input at system boundaries
- Parameterized queries only — no SQL string concatenation
- Rate limiting on all API endpoints
- CORS, CSRF, XSS protection on all routes
- Container image scanning before deployment
- Secret scanning in pre-commit hooks
- TLS everywhere in production
