"""Order management API routes."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/orders", tags=["orders"])

class OrderItemCreate(BaseModel):
    product_id: UUID
    quantity: int = 1

class OrderCreate(BaseModel):
    items: list[OrderItemCreate]

@router.post("")
async def create_order(order_data: OrderCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Create a new order."""
    total = 0.0
    order_items = []
    for item in order_data.items:
        product = await db.get(Product, item.product_id)
        if not product or not product.is_active:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        total += product.price * item.quantity
        order_items.append(OrderItem(product_id=product.id, price=product.price, quantity=item.quantity))
    order = Order(user_id=user.id, total=total, status=OrderStatus.pending)
    order.items = order_items
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

@router.get("")
async def list_orders(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """List current user's orders."""
    result = await db.execute(select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc()))
    return result.scalars().all()

@router.get("/{order_id}")
async def get_order(order_id: UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get order detail with download links."""
    order = await db.get(Order, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
