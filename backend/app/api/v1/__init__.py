"""API v1 — versioned endpoint handlers.

Aggregates all sub-routers under a single ``v1_router`` that is
included in the main FastAPI app with the ``/api/v1`` prefix.
"""

from fastapi import APIRouter

from app.api.v1.agents import router as agents_router
from app.api.v1.auth import router as auth_router
from app.api.v1.tenants import router as tenants_router
from app.api.v1.users import router as users_router

v1_router = APIRouter()
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(tenants_router)
v1_router.include_router(agents_router)
