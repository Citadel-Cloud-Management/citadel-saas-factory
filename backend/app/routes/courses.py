"""Course and enrollment API routes."""
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.course import Course, Enrollment
from app.models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("")
async def list_courses(db: AsyncSession = Depends(get_db)):
    """List all available courses."""
    result = await db.execute(select(Course))
    return result.scalars().all()

@router.get("/{slug}")
async def get_course(slug: str, db: AsyncSession = Depends(get_db)):
    """Get course detail with modules."""
    result = await db.execute(select(Course).where(Course.slug == slug))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/{slug}/enroll")
async def enroll(slug: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Enroll user in a course."""
    result = await db.execute(select(Course).where(Course.slug == slug))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    existing = await db.execute(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course.id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already enrolled")
    enrollment = Enrollment(user_id=user.id, course_id=course.id)
    db.add(enrollment)
    await db.commit()
    return {"message": "Enrolled successfully", "course": course.title}

class ProgressUpdate(BaseModel):
    module_id: str
    completed: bool

@router.put("/{slug}/progress")
async def update_progress(slug: str, data: ProgressUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Update course progress."""
    result = await db.execute(select(Course).where(Course.slug == slug))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    result = await db.execute(select(Enrollment).where(Enrollment.user_id == user.id, Enrollment.course_id == course.id))
    enrollment = result.scalar_one_or_none()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Not enrolled")
    progress = dict(enrollment.progress or {})
    progress[data.module_id] = data.completed
    enrollment.progress = progress
    await db.commit()
    return {"progress": progress}
