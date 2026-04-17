"""Prometheus metrics middleware."""

import time

from fastapi import Request
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)


def _get_route_template(request: Request) -> str:
    """Get the route template path to avoid label cardinality explosion."""
    route = request.scope.get("route")
    if route and hasattr(route, "path"):
        return route.path
    return request.url.path


class MetricsMiddleware(BaseHTTPMiddleware):
    """Collect request count and latency metrics for Prometheus."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            raise
        finally:
            duration = time.perf_counter() - start_time
            path = _get_route_template(request)
            REQUEST_COUNT.labels(
                method=request.method,
                path=path,
                status=status_code,
            ).inc()
            REQUEST_LATENCY.labels(
                method=request.method,
                path=path,
            ).observe(duration)

        response.headers["X-Response-Time"] = f"{duration:.4f}"
        return response
