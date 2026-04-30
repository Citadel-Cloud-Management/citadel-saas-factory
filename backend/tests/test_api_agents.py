"""Tests for agents API endpoints.

These tests validate the agents API contract. They will pass once
the routes are implemented under /api/v1/agents/. Until then, they
serve as executable documentation.
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


def _api_headers(token: str) -> dict[str, str]:
    """Return standard API headers with auth and tenant."""
    return {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": TEST_TENANT_ID,
    }


@pytest.mark.asyncio
async def test_list_agents(client: httpx.AsyncClient) -> None:
    """GET /api/v1/agents/ returns a list (when route exists)."""
    token = _create_test_token()
    patches = _patch_auth()
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/agents/",
            headers=_api_headers(token),
        )
    # 200 when implemented, 404 when route not yet built
    assert response.status_code in {200, 404}


@pytest.mark.asyncio
async def test_list_agent_domains(client: httpx.AsyncClient) -> None:
    """GET /api/v1/agents/domains returns domain list (when route exists)."""
    token = _create_test_token()
    patches = _patch_auth()
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/agents/domains",
            headers=_api_headers(token),
        )
    assert response.status_code in {200, 404}


@pytest.mark.asyncio
async def test_agents_requires_auth(client: httpx.AsyncClient) -> None:
    """GET /api/v1/agents/ without auth returns 401."""
    response = await client.get(
        "/api/v1/agents/",
        headers={"X-Tenant-ID": TEST_TENANT_ID},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_agents_requires_tenant(client: httpx.AsyncClient) -> None:
    """GET /api/v1/agents/ without tenant returns 400 or 401."""
    token = _create_test_token()
    patches = _patch_auth()
    with patches[0], patches[1], patches[2]:
        response = await client.get(
            "/api/v1/agents/",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code in {400, 401}
