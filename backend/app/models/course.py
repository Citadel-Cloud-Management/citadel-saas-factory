"""Course and Enrollment models."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, default="")
    modules = Column(JSON, default=list)
    is_free = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    enrollments = relationship("Enrollment", back_populates="course", lazy="selectin")

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False, index=True)
    progress = Column(JSON, default=dict)
    completed_at = Column(DateTime, nullable=True)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    course = relationship("Course", back_populates="enrollments")
