from sqlalchemy.orm import Session
from app.db.repository.courseRepo import CourseRepository
from app.db.repository.lessonRepo import LessonRepository
from app.db.repository.progressRepo import ProgressRepository
from app.db.schemas.course import CourseCreate, CourseUpdate, CourseWithProgress
from app.db.models.user import User
from typing import List
from fastapi import HTTPException, status


class CourseService:
    def __init__(self, db: Session):
        self.course_repo = CourseRepository(db)
        self.lesson_repo = LessonRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.db = db
    
    def create_course(self, course_data: CourseCreate):
        return self.course_repo.create_course(course_data)
    
    def get_course_by_id(self, course_id: int):
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        return course
    
    def get_all_courses(self):
        return self.course_repo.get_all_courses()
    
    def get_courses_with_progress(self, user: User) -> List[CourseWithProgress]:
        courses = self.course_repo.get_all_courses()
        result = []
        
        for course in courses:
            total_lessons = self.lesson_repo.count_lessons_by_course_id(course.id)
            completed_lessons = self.progress_repo.count_completed_lessons_by_course(user.id, course.id)
            
            progress_percentage = (
                (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0.0
            )
            
            course_dict = {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "created_at": course.created_at,
                "updated_at": course.updated_at,
                "progress_percentage": round(progress_percentage, 2),
                "total_lessons": total_lessons,
                "completed_lessons": completed_lessons
            }
            result.append(CourseWithProgress(**course_dict))
        
        return result
    
    def update_course(self, course_id: int, course_data: CourseUpdate):
        course = self.course_repo.update_course(course_id, course_data)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        return course
    
    def delete_course(self, course_id: int):
        if not self.course_repo.delete_course(course_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        return {"message": "Course deleted successfully"}

