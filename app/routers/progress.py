from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security.authHandler import get_current_user
from app.db.models.user import User
from app.db.schemas.progress import ProgressOutput, ProgressSummary
from app.service.progressService import ProgressService
from pydantic import BaseModel

progressRouter = APIRouter()


class CompleteLessonRequest(BaseModel):
    lesson_id: int


@progressRouter.post("/complete", response_model=ProgressOutput, status_code=status.HTTP_200_OK)
async def complete_lesson(
    request: CompleteLessonRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    progress_service = ProgressService(db)
    return progress_service.complete_lesson(current_user, request.lesson_id)


@progressRouter.get("/my", response_model=List[ProgressSummary])
async def get_my_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    progress_service = ProgressService(db)
    return progress_service.get_user_progress_summary(current_user)


@progressRouter.get("/recommended")
async def get_recommended_course(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    progress_service = ProgressService(db)
    course = progress_service.get_recommended_course(current_user)
    
    if not course:
        return {"message": "No courses available"}
    
    return {
        "course_id": course.id,
        "title": course.title,
        "description": course.description
    }

