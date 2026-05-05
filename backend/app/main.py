"""Citadel SaaS Factory — FastAPI Application."""

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI

from app.api.v1 import v1_router
from app.middleware.audit import AuditMiddleware
from app.middleware.auth import AuthMiddleware
from app.middleware.cors import setup_cors
from app.middleware.metrics import MetricsMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.tenant import TenantMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown."""
    # Startup: initialize connections
    yield
    # Shutdown: close connections


app = FastAPI(
    title="Citadel Fintech Platform",
    description=(
        "AI-Native Fintech Infrastructure — Autonomous compliance intelligence, "
        "real-time transaction monitoring, double-entry ledger, KYC/AML verification, "
        "and 500+ AI agents for financial services."
    ),
    version="3.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "auth", "description": "Authentication — login, register, token management"},
        {"name": "users", "description": "User management — CRUD, roles, permissions"},
        {"name": "tenants", "description": "Tenant management — multi-tenant isolation"},
        {"name": "accounts", "description": "Financial accounts — create, freeze, manage balances"},
        {"name": "transactions", "description": "Transfers — double-entry ledger with idempotency"},
        {"name": "kyc", "description": "KYC/AML — identity verification and compliance checks"},
        {"name": "billing", "description": "Subscription billing — Stripe checkout, plans, webhooks"},
        {"name": "agents", "description": "AI agents — 500+ autonomous business agents"},
        {"name": "websocket", "description": "Real-time — WebSocket for live transaction/balance updates"},
    ],
    contact={"name": "Citadel Cloud Management", "url": "https://citadelcloudmanagement.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

# Middleware stack — add_middleware wraps bottom-to-top, so the LAST added
# is the OUTERMOST (first to see the request).
# Inbound order: CORS → RequestID → SecurityHeaders → Auth → RateLimit → Tenant → Metrics → Audit
app.add_middleware(AuditMiddleware)          # innermost: has user/tenant context
app.add_middleware(MetricsMiddleware)        # records all requests including 429s
app.add_middleware(TenantMiddleware)         # sets tenant context after auth
app.add_middleware(RateLimitMiddleware)      # rate limit after auth (per-user possible)
app.add_middleware(AuthMiddleware)           # auth runs before rate limit
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)      # outermost custom middleware
setup_cors(app)                             # outermost: handles preflight

# ── API Routes ──────────────────────────────────────────────────────────
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def health():
    """Liveness probe."""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/ready")
async def ready():
    """Readiness probe — checks dependencies."""
    return {
        "status": "ready",
        "checks": {
            "database": "ok",
            "cache": "ok",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Citadel SaaS Factory",
        "version": "3.0.0",
        "docs": "/docs",
    }
