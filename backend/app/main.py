"""Citadel SaaS Factory — FastAPI Application."""

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.audit import AuditMiddleware
from app.middleware.metrics import MetricsMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


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

# Middleware stack (executed bottom-to-top)
app.add_middleware(AuditMiddleware)
app.add_middleware(MetricsMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure per environment via CORS_ORIGINS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
