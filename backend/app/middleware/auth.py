"""Keycloak JWT authentication middleware."""

import os
import time
from typing import Any, Optional

import structlog
from fastapi import HTTPException, Request, status
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = structlog.get_logger("auth")

JWKS_URL = os.getenv("JWKS_URL", "")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE", "")
JWKS_CACHE_TTL_SECONDS = 300  # 5 minutes
PUBLIC_PATHS = {"/health", "/ready", "/docs", "/openapi.json", "/", "/redoc"}

_jwks_cache: dict[str, Any] | None = None
_jwks_cache_time: float = 0.0


async def fetch_jwks() -> dict[str, Any] | None:
    """Fetch JWKS asynchronously with TTL-based caching."""
    global _jwks_cache, _jwks_cache_time

    if _jwks_cache and (time.time() - _jwks_cache_time) < JWKS_CACHE_TTL_SECONDS:
        return _jwks_cache

    if not JWKS_URL:
        return None

    try:
        import httpx

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(JWKS_URL)
            response.raise_for_status()
            _jwks_cache = response.json()
            _jwks_cache_time = time.time()
            logger.info("jwks_fetched", url=JWKS_URL)
            return _jwks_cache
    except Exception as exc:
        logger.error("jwks_fetch_failed", url=JWKS_URL, error=str(exc))
        return _jwks_cache  # Return stale cache if available


def _find_rsa_key(jwks: dict[str, Any], kid: str) -> dict[str, str]:
    """Find RSA key by kid in JWKS document."""
    for key in jwks.get("keys", []):
        if key.get("kid") != kid:
            continue
        try:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
        except KeyError:
            logger.warning("jwks_key_missing_fields", kid=kid, available=list(key.keys()))
            continue
    return {}


class AuthMiddleware(BaseHTTPMiddleware):
    """Validate JWT tokens from Keycloak."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in PUBLIC_PATHS or request.method == "OPTIONS":
            return await call_next(request)

        token = _extract_bearer_token(request)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            jwks = await fetch_jwks()
            if jwks is None:
                logger.warning("jwks_not_configured", hint="Set JWKS_URL env var")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Authentication service not configured",
                )

            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            rsa_key = _find_rsa_key(jwks, kid) if kid else {}
            if not rsa_key:
                # Key rotation: try refreshing JWKS
                global _jwks_cache_time
                _jwks_cache_time = 0.0
                jwks = await fetch_jwks()
                if jwks:
                    rsa_key = _find_rsa_key(jwks, kid) if kid else {}

            if not rsa_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unable to find matching signing key",
                )

            decode_options = {"verify_aud": bool(JWT_AUDIENCE)}
            decoded = jwt.decode(
                token,
                rsa_key,
                algorithms=[JWT_ALGORITHM],
                audience=JWT_AUDIENCE or None,
                options=decode_options,
            )
            request.state.user = decoded
            request.state.user_id = decoded.get("sub")

        except JWTError as exc:
            logger.warning("jwt_validation_failed", error=str(exc))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except HTTPException:
            raise
        except Exception as exc:
            logger.error("auth_unexpected_error", error=str(exc))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication error",
            )

        return await call_next(request)


def _extract_bearer_token(request: Request) -> Optional[str]:
    """Extract Bearer token from Authorization header (case-insensitive)."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:]
    return None
