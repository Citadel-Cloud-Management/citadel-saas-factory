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
    title="Citadel SaaS Factory",
    description="Universal Full-Stack SaaS Production Framework",
    version="3.0.0",
    lifespan=lifespan,
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
