---
name: ms-security-first
description: Security-first engineering — zero trust, least privilege, RBAC, audit logging, secrets isolation, key rotation, immutable infrastructure, encryption everywhere. Threat modeling for every design.
type: directive
priority: 6
---

# Security-First Engineering

## Core Rule

All systems must be designed with security as the primary constraint. Security is never traded for convenience or speed.

## Mandatory Security Principles

### Identity & Access
- **Least privilege** — minimum permissions required for each role/service
- **Zero trust** — verify every request, trust no network boundary
- **RBAC** — role-based access control for all resources
- **Audit logging** — every access, mutation, and privilege escalation logged

### Secrets & Keys
- **Secrets isolation** — never in code, configs, or environment at rest
- **Key rotation** — automated rotation on schedule (90 days max)
- **Signed artifacts** — all deployable artifacts are signed and verified
- **Supply chain protection** — dependency verification, SBOM generation

### Infrastructure
- **Immutable infrastructure** — never patch in place, rebuild
- **Secure defaults** — deny-by-default network policies, disabled debug modes
- **Encryption in transit** — TLS 1.3 minimum, mTLS for service-to-service
- **Encryption at rest** — AES-256 for all stored data, managed KMS keys

## Threat Assessment Checklist

For every design, evaluate:

```
[ ] Attack surface — what is exposed?
[ ] Secret leakage — where could secrets escape?
[ ] Privilege escalation — can a low-priv user gain admin?
[ ] SSRF — can internal services be reached via user input?
[ ] RCE — can arbitrary code be executed?
[ ] Injection risks — SQL, command, template, LDAP?
[ ] API abuse — rate limiting, authentication bypass?
[ ] Lateral movement — can a compromised service reach others?
[ ] Container breakout — are containers properly isolated?
[ ] Cloud misconfiguration — public buckets, overly permissive IAM?
[ ] CI/CD compromise — can pipeline be poisoned?
[ ] Dependency risk — known CVEs, typosquatting?
```

## If a Design Is Unsafe

1. **Explain why** — specific vulnerability, attack vector, impact
2. **Propose safer alternatives** — concrete alternative architecture
3. **Quantify risk** — likelihood × impact assessment
4. **Provide mitigation timeline** — immediate, short-term, long-term fixes

## Security Controls Matrix

| Layer | Control | Implementation |
|-------|---------|---------------|
| Network | Segmentation | K8s NetworkPolicy, VPC subnets |
| Network | WAF | Cloudflare/AWS WAF rules |
| Application | Input validation | Schema validation (Zod, Pydantic) |
| Application | Auth | JWT + refresh tokens, short TTL |
| Application | Rate limiting | Redis-backed sliding window |
| Data | Encryption | AES-256-GCM, managed KMS |
| Data | PII handling | Tokenization, masking in logs |
| Infrastructure | Image scanning | Trivy in CI, admission control |
| Infrastructure | Policy | Kyverno/OPA for K8s |
| Secrets | Management | HashiCorp Vault, sealed secrets |
| Monitoring | SIEM | Structured logs → detection rules |

## OWASP Top 10 Coverage

Every application must be hardened against:
1. Broken Access Control → RBAC + tenant isolation
2. Cryptographic Failures → TLS + KMS + rotation
3. Injection → Parameterized queries + input validation
4. Insecure Design → Threat modeling + security reviews
5. Security Misconfiguration → IaC scanning + hardened defaults
6. Vulnerable Components → SCA scanning + SBOM
7. Auth Failures → MFA + session management + brute-force protection
8. Data Integrity Failures → Signed artifacts + verified pipelines
9. Logging Failures → Structured audit logs + alerting
10. SSRF → Allowlist outbound + network segmentation
