"""Tests for the multi-tenant context middleware."""

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


@pytest.mark.asyncio
async def test_valid_tenant_id_accepted(client: httpx.AsyncClient) -> None:
    """Request with a valid X-Tenant-ID to an API path is accepted."""
    token = _create_test_token()
    patches = _patch_auth()
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/anything",
            headers={
                "Authorization": f"Bearer {token}",
                "X-Tenant-ID": TEST_TENANT_ID,
            },
        )
    # Route does not exist -> 404 means tenant middleware passed
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_missing_tenant_id_on_api_returns_400(
    client: httpx.AsyncClient,
) -> None:
    """API request without X-Tenant-ID returns 400."""
    token = _create_test_token()
    patches = _patch_auth()
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/anything",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_invalid_tenant_id_format_returns_400(
    client: httpx.AsyncClient,
) -> None:
    """API request with an invalid tenant ID format returns 400."""
    token = _create_test_token()
    patches = _patch_auth()
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/anything",
            headers={
                "Authorization": f"Bearer {token}",
                "X-Tenant-ID": "../../invalid!",
            },
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_public_paths_skip_tenant_check(client: httpx.AsyncClient) -> None:
    """Public paths do not require X-Tenant-ID."""
    response = await client.get("/health")
    assert response.status_code == 200
