"""Keycloak JWT authentication middleware."""

import os
from typing import Optional

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

JWKS_URL = os.getenv("JWKS_URL", "")
PUBLIC_PATHS = {"/health", "/ready", "/docs", "/openapi.json"}


class AuthMiddleware(BaseHTTPMiddleware):
    """Validate JWT tokens from Keycloak via PyJWKClient."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        token = _extract_bearer_token(request)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header",
            )

        # TODO: Validate JWT using PyJWKClient against JWKS_URL
        # from jwt import PyJWKClient
        # jwks_client = PyJWKClient(JWKS_URL)
        # signing_key = jwks_client.get_signing_key_from_jwt(token)
        # decoded = jwt.decode(token, signing_key.key, algorithms=["RS256"])
        # request.state.user = decoded

        return await call_next(request)


def _extract_bearer_token(request: Request) -> Optional[str]:
    """Extract Bearer token from Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None
