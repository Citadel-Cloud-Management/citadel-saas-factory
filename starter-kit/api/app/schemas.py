from pydantic import BaseModel, EmailStr  # requires: pip install pydantic[email]


class HealthResponse(BaseModel):
    status: str
    service: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
