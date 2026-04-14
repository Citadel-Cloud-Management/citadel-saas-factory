"""Multi-tenant context middleware."""

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

TENANT_HEADER = "X-Tenant-ID"


class TenantMiddleware(BaseHTTPMiddleware):
    """Extract tenant ID and set database-level tenant context via SET LOCAL."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        tenant_id = request.headers.get(TENANT_HEADER)

        if request.url.path.startswith("/api/") and not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing {TENANT_HEADER} header",
            )

        request.state.tenant_id = tenant_id

        # TODO: Set tenant context on database connection
        # async with db.begin() as conn:
        #     await conn.execute(text(f"SET LOCAL app.tenant_id = '{tenant_id}'"))

        return await call_next(request)
