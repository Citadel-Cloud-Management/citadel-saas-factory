"""Redis sliding window rate limiter middleware."""

import os
import time

import redis.asyncio as aioredis
import structlog
from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = structlog.get_logger("rate_limit")

RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
RATE_LIMIT_FAIL_OPEN = os.getenv("RATE_LIMIT_FAIL_OPEN", "false").lower() == "true"

_redis_pool: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis:
    """Get or create async Redis connection pool."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis_pool


def _get_client_ip(request: Request) -> str:
    """Extract real client IP, accounting for reverse proxy headers."""
    forwarded = request.headers.get("X-Real-IP")
    if forwarded:
        return forwarded.strip()
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Sliding window rate limiter using Redis sorted sets."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_ip = _get_client_ip(request)
        key = f"rate_limit:{client_ip}"
        remaining = RATE_LIMIT

        try:
            r = await get_redis()
            now = time.time()
            window_start = now - 60

            # Atomic pipeline: clean old entries, check count, conditionally add
            pipe = r.pipeline()
            pipe.zremrangebyscore(key, 0, f"({window_start}")
            pipe.zcard(key)
            results = await pipe.execute()
            count = results[1]

            if count >= RATE_LIMIT:
                remaining = 0
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded",
                )

            # Under limit — add this request
            pipe2 = r.pipeline()
            pipe2.zadd(key, {f"{now}:{id(request)}": now})
            pipe2.expire(key, 60)
            await pipe2.execute()

            remaining = max(0, RATE_LIMIT - count - 1)

        except HTTPException:
            raise
        except Exception as exc:
            if RATE_LIMIT_FAIL_OPEN:
                logger.error("rate_limit_redis_error", error=str(exc), policy="fail_open")
            else:
                logger.error("rate_limit_redis_error", error=str(exc), policy="fail_closed")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Rate limiting service unavailable",
                )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
