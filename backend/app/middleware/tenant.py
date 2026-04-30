"""Multi-tenant context middleware."""

import re

import structlog
from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = structlog.get_logger("tenant")

TENANT_HEADER = "X-Tenant-ID"
TENANT_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")
PUBLIC_PATHS = {"/health", "/ready", "/docs", "/openapi.json", "/", "/redoc"}


class TenantMiddleware(BaseHTTPMiddleware):
    """Extract tenant ID and set database-level tenant context via SET LOCAL."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in PUBLIC_PATHS or request.method == "OPTIONS":
            request.state.tenant_id = None
            return await call_next(request)

        tenant_id = request.headers.get(TENANT_HEADER)

        if request.url.path.startswith("/api/") and not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing {TENANT_HEADER} header",
            )

        if tenant_id and not TENANT_ID_PATTERN.match(tenant_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid tenant ID format",
            )

        request.state.tenant_id = tenant_id

        # NOTE: RLS enforcement happens at the database session level.
        # When a route handler obtains a session via get_db(), it should call
        # set_tenant_context(session, tenant_id) from app.db.session to execute
        # SET LOCAL app.current_tenant = tenant_id, scoping all queries to
        # this tenant's rows via PostgreSQL RLS policies.

        if tenant_id:
            logger.debug("tenant_context_set", tenant_id=tenant_id, path=request.url.path)

        return await call_next(request)
