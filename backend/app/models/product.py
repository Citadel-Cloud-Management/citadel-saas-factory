"""Product model for digital downloads."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, default="")
    price = Column(Float, default=0.0)
    compare_at_price = Column(Float, nullable=True)
    product_type = Column(String(100), default="toolkit")
    collection = Column(String(100), index=True)
    tags = Column(JSON, default=list)
    download_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.title}>"
