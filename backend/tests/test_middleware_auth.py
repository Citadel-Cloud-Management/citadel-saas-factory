"""Tests for the JWT authentication middleware."""

from datetime import timedelta
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from jose import jwt

from tests.conftest import (
    TEST_JWT_ALGORITHM,
    TEST_JWT_SECRET,
    TEST_USER_ID,
    _create_test_token,
)


# ---------------------------------------------------------------------------
# Helper: build a JWKS document that matches tokens signed with HS256.
# The real middleware expects RS256 + JWKS, so we patch `fetch_jwks` and
# `jwt.decode` to isolate the middleware logic from Keycloak.
# ---------------------------------------------------------------------------


def _patch_auth_to_use_hs256(token: str | None = None):
    """Context manager that patches the auth middleware to accept HS256 tokens."""

    async def _fake_fetch_jwks():
        return {"keys": [{"kid": "test-kid", "kty": "oct"}]}

    def _fake_decode(tok, _key, algorithms, audience=None, options=None):
        return jwt.decode(tok, TEST_JWT_SECRET, algorithms=[TEST_JWT_ALGORITHM])

    return (
        patch("app.middleware.auth.fetch_jwks", side_effect=_fake_fetch_jwks),
        patch("app.middleware.auth._find_rsa_key", return_value={"kid": "test-kid"}),
        patch("app.middleware.auth.jwt.decode", side_effect=_fake_decode),
    )


@pytest.mark.asyncio
async def test_missing_auth_header_returns_401(client: httpx.AsyncClient) -> None:
    """Protected endpoint without Authorization header returns 401."""
    response = await client.get(
        "/api/v1/anything",
        headers={"X-Tenant-ID": "test-tenant"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_jwt_returns_401(client: httpx.AsyncClient) -> None:
    """Request with a malformed JWT returns 401."""
    patches = _patch_auth_to_use_hs256()
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/anything",
            headers={
                "Authorization": "Bearer invalid.token.here",
                "X-Tenant-ID": "test-tenant",
            },
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_expired_jwt_returns_401(
    client: httpx.AsyncClient,
    expired_token: str,
) -> None:
    """Request with an expired JWT returns 401."""
    patches = _patch_auth_to_use_hs256()
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/anything",
            headers={
                "Authorization": f"Bearer {expired_token}",
                "X-Tenant-ID": "test-tenant",
            },
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_valid_jwt_passes_through(client: httpx.AsyncClient) -> None:
    """Request with a valid JWT passes auth and hits downstream middleware/routes."""
    token = _create_test_token()
    patches = _patch_auth_to_use_hs256(token)
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/anything",
            headers={
                "Authorization": f"Bearer {token}",
                "X-Tenant-ID": "test-tenant",
            },
        )
    # The route does not exist, so we expect 404 (auth passed).
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_public_paths_skip_auth(client: httpx.AsyncClient) -> None:
    """Public paths (/, /health, /ready, /docs) do not require auth."""
    for path in ["/", "/health", "/ready"]:
        response = await client.get(path)
        assert response.status_code == 200, f"{path} should be public"
