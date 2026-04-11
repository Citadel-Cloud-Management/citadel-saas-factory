"""Product catalog API routes."""
from uuid import UUID
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.product import Product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("")
async def list_products(
    collection: str | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(24, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List products with filtering and pagination."""
    query = select(Product).where(Product.is_active == True)
    if collection:
        query = query.where(Product.collection == collection)
    if search:
        query = query.where(Product.title.ilike(f"%{search}%"))
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    return {"products": products, "total": total, "page": page, "limit": limit}

@router.get("/{slug}")
async def get_product(slug: str, db: AsyncSession = Depends(get_db)):
    """Get single product by slug."""
    result = await db.execute(select(Product).where(Product.slug == slug, Product.is_active == True))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/collection/{handle}")
async def get_by_collection(handle: str, page: int = Query(1, ge=1), limit: int = Query(24, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    """Get products by collection handle."""
    query = select(Product).where(Product.collection == handle, Product.is_active == True)
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(query.offset((page - 1) * limit).limit(limit))
    return {"products": result.scalars().all(), "total": total, "page": page}
