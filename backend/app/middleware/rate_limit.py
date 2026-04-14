"""Redis sliding window rate limiter middleware."""

import os
import time

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Sliding window rate limiter using Redis sorted sets."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:{client_ip}"

        # TODO: Implement Redis sliding window
        # async with redis_pool.client() as redis:
        #     now = time.time()
        #     window_start = now - 60
        #     pipe = redis.pipeline()
        #     pipe.zremrangebyscore(key, 0, window_start)
        #     pipe.zadd(key, {str(now): now})
        #     pipe.zcard(key)
        #     pipe.expire(key, 60)
        #     _, _, count, _ = await pipe.execute()
        #     if count > RATE_LIMIT:
        #         raise HTTPException(status_code=429, detail="Rate limit exceeded")

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
        return response
