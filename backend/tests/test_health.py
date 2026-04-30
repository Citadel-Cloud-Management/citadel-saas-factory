"""Tests for health, readiness, and root endpoints."""

import httpx
import pytest


@pytest.mark.asyncio
async def test_root_returns_welcome(client: httpx.AsyncClient) -> None:
    """GET / returns 200 with application name."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Citadel SaaS Factory"
    assert "version" in data


@pytest.mark.asyncio
async def test_health_returns_healthy(client: httpx.AsyncClient) -> None:
    """GET /health returns 200 with status healthy."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_ready_returns_ready(client: httpx.AsyncClient) -> None:
    """GET /ready returns 200 with status ready."""
    response = await client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "checks" in data
    assert data["checks"]["database"] == "ok"
    assert data["checks"]["cache"] == "ok"
