"""Citadel SaaS Factory — FastAPI Application."""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.auth import router as auth_router
from app.routes.products import router as products_router
from app.routes.orders import router as orders_router
from app.routes.courses import router as courses_router
from app.routes.webhooks import router as webhooks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="Citadel SaaS Factory",
    description="Cloud education and digital products platform API",
    version="3.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(courses_router)
app.include_router(webhooks_router)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "citadel-saas-factory"}

@app.get("/ready")
async def ready():
    return {"status": "ready"}
