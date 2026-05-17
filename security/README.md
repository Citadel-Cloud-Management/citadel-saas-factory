# Security

Security tooling, policies, and detection rules for defense-in-depth.

| Tool | Directory | Purpose |
|------|-----------|---------|
| Falco | `falco/` | Runtime threat detection (kernel-level) |
| Kyverno | `kyverno/` | Kubernetes admission policies |
| Guardrails AI | `guardrails/` | LLM output validation |
| OPA | `opa/` | Open Policy Agent rules |
| Trivy | `trivy/` | Container vulnerability scanning |
| Sigma | `sigma/` | Detection rules (SIEM integration) |

## Guardrails Stack

Every LLM call passes through triple-layer validation:
1. **Guardrails AI** — Schema enforcement, hallucination detection
2. **NeMo Guardrails** — Dialogue control, trust scoring
3. **DeepEval** — Continuous monitoring in CI/CD

Score >= 0.85 passes. Score < 0.85 retries (max 3), then rejects.

## Run Security Scan

```bash
make security        # Full scan
trivy image backend  # Container scan
semgrep --config auto backend/  # SAST
```
