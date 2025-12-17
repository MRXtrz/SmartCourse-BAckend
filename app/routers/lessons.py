from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security.authHandler import get_current_user, get_current_admin_user
from app.db.models.user import User
from app.db.schemas.lesson import LessonCreate, LessonUpdate, LessonOutput, LessonWithProgress
from app.service.lessonService import LessonService

lessonsRouter = APIRouter()


@lessonsRouter.get("/courses/{course_id}/lessons", response_model=List[LessonWithProgress])
async def get_lessons_by_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson_service = LessonService(db)
    return lesson_service.get_lessons_by_course_id(course_id, current_user)


@lessonsRouter.get("/{lesson_id}", response_model=LessonOutput)
async def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):
    lesson_service = LessonService(db)
    return lesson_service.get_lesson_by_id(lesson_id)


@lessonsRouter.post("", response_model=LessonOutput, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    lesson_data: LessonCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    lesson_service = LessonService(db)
    return lesson_service.create_lesson(lesson_data)


@lessonsRouter.put("/{lesson_id}", response_model=LessonOutput)
async def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    lesson_service = LessonService(db)
    return lesson_service.update_lesson(lesson_id, lesson_data)


@lessonsRouter.delete("/{lesson_id}", status_code=status.HTTP_200_OK)
async def delete_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    lesson_service = LessonService(db)
    return lesson_service.delete_lesson(lesson_id)

