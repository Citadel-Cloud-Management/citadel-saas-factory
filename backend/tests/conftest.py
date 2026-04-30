"""Pytest fixtures for Citadel SaaS Factory backend tests."""

from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi import FastAPI
from jose import jwt

from app.main import app as _app


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------

TEST_JWT_SECRET = "test-secret-key-for-unit-tests-only"  # noqa: S105
TEST_JWT_ALGORITHM = "HS256"
TEST_USER_ID = "user-00000000-0000-0000-0000-000000000001"
TEST_TENANT_ID = "test-tenant-001"


def _create_test_token(
    sub: str = TEST_USER_ID,
    exp_delta: timedelta | None = None,
    extra_claims: dict | None = None,
) -> str:
    """Create a signed HS256 JWT for testing."""
    now = datetime.now(timezone.utc)
    claims = {
        "sub": sub,
        "iat": now,
        "exp": now + (exp_delta or timedelta(hours=1)),
        "email": "test@citadel.dev",
        "roles": ["user"],
    }
    if extra_claims:
        claims.update(extra_claims)
    return jwt.encode(claims, TEST_JWT_SECRET, algorithm=TEST_JWT_ALGORITHM)


# ---------------------------------------------------------------------------
# Application fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def app() -> FastAPI:
    """Return the FastAPI application instance."""
    return _app


# ---------------------------------------------------------------------------
# Async HTTP client
# ---------------------------------------------------------------------------


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide an httpx AsyncClient bound to the test app.

    The middleware stack uses BaseHTTPMiddleware, so we patch external
    dependencies (Redis, JWKS) to keep tests self-contained.
    """
    # Patch Redis to avoid real connections in rate-limit middleware
    mock_redis = AsyncMock()
    mock_redis.pipeline.return_value = _mock_pipeline()

    with (
        patch("app.middleware.rate_limit.get_redis", return_value=mock_redis),
        patch("app.middleware.rate_limit._redis_pool", mock_redis),
    ):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as ac:
            yield ac


def _mock_pipeline() -> AsyncMock:
    """Return a mock Redis pipeline that always succeeds."""
    pipe = AsyncMock()
    pipe.zremrangebyscore = AsyncMock()
    pipe.zcard = AsyncMock()
    pipe.zadd = AsyncMock()
    pipe.expire = AsyncMock()
    pipe.execute = AsyncMock(return_value=[0, 0])
    return pipe


# ---------------------------------------------------------------------------
# Auth / tenant header helpers
# ---------------------------------------------------------------------------


@pytest.fixture()
def auth_headers() -> dict[str, str]:
    """Headers with a valid test JWT (HS256-signed)."""
    token = _create_test_token()
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def tenant_headers() -> dict[str, str]:
    """Headers with a valid X-Tenant-ID."""
    return {"X-Tenant-ID": TEST_TENANT_ID}


@pytest.fixture()
def expired_token() -> str:
    """Return an expired JWT token string."""
    return _create_test_token(exp_delta=timedelta(hours=-1))
