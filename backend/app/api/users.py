"""User management endpoints."""
from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.user import TenantResponse, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.get("/me/tenant", response_model=TenantResponse)
async def get_my_tenant(user: User = Depends(get_current_user)):
    return user.tenant
