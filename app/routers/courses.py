from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security.authHandler import get_current_user, get_current_admin_user
from app.db.models.user import User
from app.db.schemas.course import CourseCreate, CourseUpdate, CourseOutput, CourseWithProgress
from app.service.courseService import CourseService

coursesRouter = APIRouter()


@coursesRouter.get("", response_model=List[CourseWithProgress])
async def get_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    course_service = CourseService(db)
    return course_service.get_courses_with_progress(current_user)


@coursesRouter.get("/{course_id}", response_model=CourseOutput)
async def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course_service = CourseService(db)
    return course_service.get_course_by_id(course_id)


@coursesRouter.post("", response_model=CourseOutput, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    course_service = CourseService(db)
    return course_service.create_course(course_data)


@coursesRouter.put("/{course_id}", response_model=CourseOutput)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    course_service = CourseService(db)
    return course_service.update_course(course_id, course_data)


@coursesRouter.delete("/{course_id}", status_code=status.HTTP_200_OK)
async def delete_course(
    course_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    course_service = CourseService(db)
    return course_service.delete_course(course_id)

