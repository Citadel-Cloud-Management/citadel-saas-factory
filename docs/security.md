# Security Guide

Comprehensive security practices for Citadel SaaS Factory.

## Security Architecture

```
                         Internet
                            |
                     +------v------+
                     |   Traefik   |  TLS termination, rate limiting
                     +------+------+
                            |
                     +------v------+
                     |   Linkerd   |  mTLS (service-to-service)
                     +------+------+
                            |
              +-------------+-------------+
              |             |             |
         +----v----+  +----v----+  +----v----+
         | FastAPI |  | Next.js |  | Keycloak|
         | (Auth,  |  | (CSP,   |  | (OAuth2,|
         |  RBAC)  |  |  XSS)   |  |  MFA)   |
         +----+----+  +---------+  +---------+
              |
    +---------+---------+
    |         |         |
+---v---+ +--v--+ +---v---+
|Postgre| |Redis| | MinIO |
| (RLS) | |(ACL)| |(IAM)  |
+-------+ +-----+ +-------+
```

## Secret Management with HashiCorp Vault

### Overview

All secrets in production are managed through HashiCorp Vault. No secrets are stored in environment variables, config files, or source code in production.

### Secret Hierarchy

```
vault/
  secret/
    citadel/
      production/
        database/       # PostgreSQL credentials
        redis/          # Redis password
        keycloak/       # Admin credentials, client secrets
        minio/          # Access key, secret key
        rabbitmq/       # User credentials
        stripe/         # API keys
        anthropic/      # API key
      staging/
        ...             # Same structure, different values
```

### Accessing Secrets

Applications retrieve secrets at startup via the Vault Agent sidecar:

```yaml
# Kubernetes pod annotation
vault.hashicorp.com/agent-inject: "true"
vault.hashicorp.com/role: "citadel-backend"
vault.hashicorp.com/agent-inject-secret-db: "secret/citadel/production/database"
```

### Secret Rotation

| Secret Type | Rotation Period | Method |
|-------------|----------------|--------|
| Database passwords | 90 days | Vault dynamic secrets |
| API keys | 90 days | Manual rotation + Vault update |
| TLS certificates | Auto-renewed | Let's Encrypt via Traefik |
| Service mesh certs | 24 hours | Linkerd auto-rotation |
| Keycloak client secrets | 90 days | Vault static secrets |

### Development Secrets

For local development, use `.env` files (never committed to git):

```bash
cp .env.example .env
# Edit .env with local development values
```

The `.gitignore` file includes `.env` and all secret patterns.

## Static Application Security Testing (SAST)

### Semgrep

Semgrep runs on every pull request to detect security vulnerabilities:

```bash
# Run locally
semgrep --config=auto --config=p/security-audit .

# CI/CD integration
# See .github/workflows/ci-cd.yml
```

Rules include:

- SQL injection detection
- XSS vulnerability patterns
- Hardcoded secrets
- Insecure cryptography
- SSRF patterns
- Path traversal

### Custom Rules

Project-specific Semgrep rules are defined in `.semgrep/`:

```yaml
rules:
  - id: no-raw-sql
    patterns:
      - pattern: db.execute($SQL)
      - pattern-not: db.execute($SQL, $PARAMS)
    message: "Use parameterized queries to prevent SQL injection"
    severity: ERROR
```

## Dynamic Application Security Testing (DAST)

### OWASP ZAP

ZAP runs against staging after each deployment:

```bash
# Baseline scan
zap-baseline.py -t https://staging.citadelcloudmanagement.com

# Full scan (nightly)
zap-full-scan.py -t https://staging.citadelcloudmanagement.com
```

### Nightly Security Scan

The nightly security workflow (`.github/workflows/nightly-security.yml`) runs:

1. ZAP full scan against staging
2. Trivy container image scan
3. TruffleHog secret scan on git history
4. Dependency vulnerability check

## Kubernetes Security

### Kyverno Policies

Kyverno enforces security policies at the cluster level:

```yaml
# Require non-root containers
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-non-root
spec:
  validationFailureAction: enforce
  rules:
    - name: check-non-root
      match:
        resources:
          kinds: ["Pod"]
      validate:
        message: "Containers must not run as root"
        pattern:
          spec:
            containers:
              - securityContext:
                  runAsNonRoot: true
```

Policies enforced:

- No root containers
- No privileged containers
- Read-only root filesystem
- Resource limits required
- No latest image tags
- Approved image registries only
- No host network/PID/IPC

### Falco Runtime Security

Falco monitors runtime behavior and alerts on suspicious activity:

```yaml
# Custom Falco rules
- rule: Detect Shell in Container
  desc: Alert when a shell is spawned in a container
  condition: >
    spawned_process and container and
    proc.name in (bash, sh, zsh)
  output: >
    Shell spawned in container
    (user=%user.name container=%container.name
     image=%container.image.repository)
  priority: WARNING
```

Falco alerts on:

- Shell access in production containers
- Unexpected network connections
- File system modifications in read-only paths
- Privilege escalation attempts
- Crypto mining processes

## Application Security

### Authentication (Keycloak)

- OAuth2 / OpenID Connect for all authentication
- Multi-Factor Authentication (MFA) enforced for admin accounts
- Session timeout: 30 minutes idle, 8 hours absolute
- Brute force protection: account lockout after 5 failed attempts
- Password policy: minimum 12 characters, complexity requirements

### Authorization (RBAC)

```
Roles:
  super_admin    --> Full access to all tenants and system config
  tenant_admin   --> Full access within own tenant
  member         --> Standard access within own tenant
  viewer         --> Read-only access within own tenant
  api_service    --> Service-to-service access (machine accounts)
```

### Input Validation

All user input is validated at system boundaries using Pydantic models:

```python
class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=255)
    role: Literal["admin", "member", "viewer"]

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        return bleach.clean(v)
```

### Rate Limiting

All API endpoints are rate-limited:

| Endpoint Type | Rate Limit |
|---------------|-----------|
| Authentication | 10 requests/minute |
| API (authenticated) | 100 requests/minute |
| API (unauthenticated) | 20 requests/minute |
| Webhooks | 50 requests/minute |
| File upload | 10 requests/minute |

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Never use ["*"] in production
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=600,
)
```

### Content Security Policy

The Next.js frontend enforces a strict CSP:

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-{random}';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.citadelcloudmanagement.com;
  frame-ancestors 'none';
```

## Compliance

### GDPR

- Data processing agreements (DPA) for all sub-processors
- Right to erasure implemented (hard delete on request)
- Data export in machine-readable format (JSON)
- Cookie consent management
- Privacy policy auto-generated and versioned

### SOC 2 Type II

- Access control policies documented and enforced
- Audit logging for all administrative actions
- Change management via GitOps (full audit trail)
- Incident response procedures documented
- Regular security assessments

## Security Checklist

Before every release:

- [ ] No hardcoded secrets in source code
- [ ] All user inputs validated with Pydantic schemas
- [ ] Parameterized queries only (no SQL string concatenation)
- [ ] Rate limiting configured on new endpoints
- [ ] CORS origins explicitly listed (no wildcards)
- [ ] Container images scanned with Trivy
- [ ] Semgrep SAST passed with zero HIGH/CRITICAL findings
- [ ] TruffleHog secret scan passed
- [ ] Kyverno policies validated
- [ ] Keycloak roles and permissions reviewed
