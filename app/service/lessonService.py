from sqlalchemy.orm import Session
from app.db.repository.lessonRepo import LessonRepository
from app.db.repository.courseRepo import CourseRepository
from app.db.repository.progressRepo import ProgressRepository
from app.db.schemas.lesson import LessonCreate, LessonUpdate, LessonWithProgress
from app.db.models.user import User
from typing import List
from fastapi import HTTPException, status


class LessonService:
    def __init__(self, db: Session):
        self.lesson_repo = LessonRepository(db)
        self.course_repo = CourseRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.db = db
    
    def create_lesson(self, lesson_data: LessonCreate):
        course = self.course_repo.get_course_by_id(lesson_data.course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        return self.lesson_repo.create_lesson(lesson_data)
    
    def get_lesson_by_id(self, lesson_id: int):
        lesson = self.lesson_repo.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
        return lesson
    
    def get_lessons_by_course_id(self, course_id: int, user: User = None) -> List:
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        lessons = self.lesson_repo.get_lessons_by_course_id(course_id)
        
        if user:
            result = []
            for lesson in lessons:
                progress = self.progress_repo.get_progress_by_user_and_lesson(user.id, lesson.id)
                lesson_dict = {
                    "id": lesson.id,
                    "course_id": lesson.course_id,
                    "title": lesson.title,
                    "content": lesson.content,
                    "created_at": lesson.created_at,
                    "updated_at": lesson.updated_at,
                    "completed": progress.completed if progress else False
                }
                result.append(LessonWithProgress(**lesson_dict))
            return result
        
        return lessons
    
    def update_lesson(self, lesson_id: int, lesson_data: LessonUpdate):
        lesson = self.lesson_repo.update_lesson(lesson_id, lesson_data)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
        return lesson
    
    def delete_lesson(self, lesson_id: int):
        if not self.lesson_repo.delete_lesson(lesson_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
        return {"message": "Lesson deleted successfully"}

