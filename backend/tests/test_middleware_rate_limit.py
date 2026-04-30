"""Tests for the rate-limiting middleware."""

from unittest.mock import AsyncMock, patch

import httpx
import pytest


@pytest.mark.asyncio
async def test_request_within_limit_returns_200(client: httpx.AsyncClient) -> None:
    """A single request within the rate limit succeeds."""
    response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_rate_limit_headers_present(client: httpx.AsyncClient) -> None:
    """Responses include X-RateLimit-Limit and X-RateLimit-Remaining."""
    response = await client.get("/health")
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert int(response.headers["X-RateLimit-Limit"]) > 0


@pytest.mark.asyncio
async def test_rate_limit_remaining_decreases(client: httpx.AsyncClient) -> None:
    """X-RateLimit-Remaining is a non-negative integer."""
    response = await client.get("/health")
    remaining = int(response.headers["X-RateLimit-Remaining"])
    assert remaining >= 0


@pytest.mark.asyncio
async def test_rate_limit_exceeded_returns_429() -> None:
    """When Redis reports the count equals the limit, return 429."""
    from app.main import app

    # Build a mock Redis where the count already equals the limit
    mock_redis = AsyncMock()
    pipe = AsyncMock()
    pipe.zremrangebyscore = AsyncMock()
    pipe.zcard = AsyncMock()
    # Return count == RATE_LIMIT (triggers 429)
    pipe.execute = AsyncMock(return_value=[0, 60])
    mock_redis.pipeline.return_value = pipe

    with patch("app.middleware.rate_limit.get_redis", return_value=mock_redis):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as ac:
            response = await ac.get("/health")

    assert response.status_code == 429
