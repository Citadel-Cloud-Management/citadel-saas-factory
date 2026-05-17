# Security Rules

## Application Security
- No hardcoded secrets — use environment variables or Vault
- Validate all user input at system boundaries
- Parameterized queries only — no SQL string concatenation
- Rate limiting on all API endpoints
- CORS, CSRF, XSS protection on all routes
- Container image scanning (Trivy) before deployment
- Secret scanning in pre-commit hooks (TruffleHog)
- TLS everywhere in production
- mTLS between all microservices via Linkerd

## AI/LLM Security (OWASP LLM Top 10)
- Every LLM call routes through `guard_llm_call()` middleware
- Treat LLM output as untrusted input — sanitize before rendering
- Never store secrets in system prompts
- Tool allowlists per agent role — deny-by-default
- HITL gates for irreversible agent actions
- Hard token/compute budgets per user/session
- Sandbox all agent code execution (gVisor/Firecracker)
- RBAC on vector databases — validate retrieved chunks before RAG injection

## Supply Chain
- ModelScan all downloaded models before production use
- SBOM generation (CycloneDX/SPDX) for all model dependencies
- Model signing (Sigstore) — verify before every deployment
- ML license compliance scanning before commercial use

## Full framework: `security/ai-security-framework.md` (11 domains, 80+ controls)
