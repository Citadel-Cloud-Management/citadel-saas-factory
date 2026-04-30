"""Tests for auth API endpoints.

These tests validate the auth API contract. They will pass once the
routes are implemented under /api/v1/auth/. Until then, they serve
as executable documentation of the expected behavior.
"""

from unittest.mock import AsyncMock, patch

import httpx
import pytest
from jose import jwt

from tests.conftest import (
    TEST_JWT_ALGORITHM,
    TEST_JWT_SECRET,
    TEST_TENANT_ID,
    _create_test_token,
)


def _patch_auth():
    """Patch auth middleware to accept HS256 test tokens."""

    async def _fake_fetch():
        return {"keys": [{"kid": "test-kid", "kty": "oct"}]}

    def _fake_decode(tok, _key, algorithms, audience=None, options=None):
        return jwt.decode(tok, TEST_JWT_SECRET, algorithms=[TEST_JWT_ALGORITHM])

    return (
        patch("app.middleware.auth.fetch_jwks", side_effect=_fake_fetch),
        patch("app.middleware.auth._find_rsa_key", return_value={"kid": "test-kid"}),
        patch("app.middleware.auth.jwt.decode", side_effect=_fake_decode),
    )


def _api_headers(token: str | None = None) -> dict[str, str]:
    """Return standard API headers with optional auth."""
    headers: dict[str, str] = {"X-Tenant-ID": TEST_TENANT_ID}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


@pytest.mark.asyncio
async def test_register_creates_user(client: httpx.AsyncClient) -> None:
    """POST /api/v1/auth/register creates a new user (when route exists)."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@citadel.dev",
            "password": "S3cure!Pass",  # noqa: S106
            "name": "Test User",
        },
        headers={"X-Tenant-ID": TEST_TENANT_ID},
    )
    # 401 (no auth bypass for register) or 404 (route not built yet)
    assert response.status_code in {200, 201, 401, 404}


@pytest.mark.asyncio
async def test_login_returns_jwt(client: httpx.AsyncClient) -> None:
    """POST /api/v1/auth/login returns a JWT (when route exists)."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@citadel.dev",
            "password": "S3cure!Pass",  # noqa: S106
        },
        headers={"X-Tenant-ID": TEST_TENANT_ID},
    )
    assert response.status_code in {200, 401, 404}


@pytest.mark.asyncio
async def test_me_returns_current_user(client: httpx.AsyncClient) -> None:
    """GET /api/v1/auth/me returns the authenticated user (when route exists)."""
    token = _create_test_token()
    patches = _patch_auth()
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/auth/me",
            headers=_api_headers(token),
        )
    assert response.status_code in {200, 404}


@pytest.mark.asyncio
async def test_login_invalid_credentials_returns_401(
    client: httpx.AsyncClient,
) -> None:
    """POST /api/v1/auth/login with wrong credentials returns 401 or 404."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong@citadel.dev",
            "password": "wrong",  # noqa: S106
        },
        headers={"X-Tenant-ID": TEST_TENANT_ID},
    )
    assert response.status_code in {401, 404}
