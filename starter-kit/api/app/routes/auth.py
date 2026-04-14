from fastapi import APIRouter
from app.schemas import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginRequest):
    return {
        "message": "Auth placeholder",
        "email": payload.email,
        "token": "replace-with-real-jwt"
    }
