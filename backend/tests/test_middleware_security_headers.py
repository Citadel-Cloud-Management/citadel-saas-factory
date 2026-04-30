"""Tests for the security headers middleware."""

import httpx
import pytest


@pytest.mark.asyncio
async def test_x_content_type_options(client: httpx.AsyncClient) -> None:
    """Response includes X-Content-Type-Options: nosniff."""
    response = await client.get("/health")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"


@pytest.mark.asyncio
async def test_x_frame_options(client: httpx.AsyncClient) -> None:
    """Response includes X-Frame-Options: DENY."""
    response = await client.get("/health")
    assert response.headers.get("X-Frame-Options") == "DENY"


@pytest.mark.asyncio
async def test_strict_transport_security(client: httpx.AsyncClient) -> None:
    """Response includes Strict-Transport-Security header."""
    response = await client.get("/health")
    hsts = response.headers.get("Strict-Transport-Security", "")
    assert "max-age=" in hsts


@pytest.mark.asyncio
async def test_content_security_policy(client: httpx.AsyncClient) -> None:
    """Response includes Content-Security-Policy header."""
    response = await client.get("/health")
    csp = response.headers.get("Content-Security-Policy", "")
    assert "default-src" in csp


@pytest.mark.asyncio
async def test_referrer_policy(client: httpx.AsyncClient) -> None:
    """Response includes Referrer-Policy header."""
    response = await client.get("/health")
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"


@pytest.mark.asyncio
async def test_x_xss_protection(client: httpx.AsyncClient) -> None:
    """Response includes X-XSS-Protection header."""
    response = await client.get("/health")
    assert "1" in response.headers.get("X-XSS-Protection", "")


@pytest.mark.asyncio
async def test_permissions_policy(client: httpx.AsyncClient) -> None:
    """Response includes Permissions-Policy header."""
    response = await client.get("/health")
    pp = response.headers.get("Permissions-Policy", "")
    assert "camera=()" in pp
