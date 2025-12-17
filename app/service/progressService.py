from sqlalchemy.orm import Session
from app.db.repository.progressRepo import ProgressRepository
from app.db.repository.lessonRepo import LessonRepository
from app.db.repository.courseRepo import CourseRepository
from app.db.schemas.progress import ProgressSummary
from app.db.models.user import User
from typing import List
from fastapi import HTTPException, status


class ProgressService:
    def __init__(self, db: Session):
        self.progress_repo = ProgressRepository(db)
        self.lesson_repo = LessonRepository(db)
        self.course_repo = CourseRepository(db)
        self.db = db
    
    def complete_lesson(self, user: User, lesson_id: int):
        lesson = self.lesson_repo.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
        
        progress = self.progress_repo.create_or_update_progress(
            user_id=user.id,
            lesson_id=lesson_id,
            course_id=lesson.course_id,
            completed=True
        )
        
        return progress
    
    def get_user_progress_summary(self, user: User) -> List[ProgressSummary]:
        courses = self.course_repo.get_all_courses()
        result = []
        
        for course in courses:
            total_lessons = self.lesson_repo.count_lessons_by_course_id(course.id)
            completed_lessons = self.progress_repo.count_completed_lessons_by_course(user.id, course.id)
            
            progress_percentage = (
                (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0.0
            )
            
            result.append(ProgressSummary(
                course_id=course.id,
                course_title=course.title,
                total_lessons=total_lessons,
                completed_lessons=completed_lessons,
                progress_percentage=round(progress_percentage, 2)
            ))
        
        return result
    
    def get_recommended_course(self, user: User):
        courses = self.course_repo.get_all_courses()
        
        if not courses:
            return None
        
        min_progress = 100.0
        recommended_course = None
        
        for course in courses:
            total_lessons = self.lesson_repo.count_lessons_by_course_id(course.id)
            if total_lessons == 0:
                continue
            
            completed_lessons = self.progress_repo.count_completed_lessons_by_course(user.id, course.id)
            progress_percentage = (completed_lessons / total_lessons * 100)
            
            if progress_percentage < min_progress:
                min_progress = progress_percentage
                recommended_course = course
        
        return recommended_course

