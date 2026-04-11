"""Order and OrderItem models."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class OrderStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    refunded = "refunded"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    total = Column(Float, default=0.0)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.pending)
    stripe_payment_intent_id = Column(String(255), nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItem", back_populates="order", lazy="selectin")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", lazy="selectin")
