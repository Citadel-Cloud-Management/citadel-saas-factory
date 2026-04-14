"""Prometheus metrics middleware."""

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

# TODO: Initialize Prometheus metrics
# from prometheus_client import Counter, Histogram
# REQUEST_COUNT = Counter("http_requests_total", "Total requests", ["method", "path", "status"])
# REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["method", "path"])


class MetricsMiddleware(BaseHTTPMiddleware):
    """Collect request count and latency metrics for Prometheus."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        # TODO: Record metrics
        # REQUEST_COUNT.labels(
        #     method=request.method,
        #     path=request.url.path,
        #     status=response.status_code,
        # ).inc()
        # REQUEST_LATENCY.labels(
        #     method=request.method,
        #     path=request.url.path,
        # ).observe(duration)

        response.headers["X-Response-Time"] = f"{duration:.4f}"
        return response
