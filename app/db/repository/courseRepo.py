from .base import BaseRepository
from app.db.models.course import Course
from app.db.schemas.course import CourseCreate, CourseUpdate
from typing import List, Optional


class CourseRepository(BaseRepository):
    def create_course(self, course_data: CourseCreate) -> Course:
        new_course = Course(**course_data.model_dump())
        self.session.add(new_course)
        self.session.commit()
        self.session.refresh(new_course)
        return new_course
    
    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        return self.session.query(Course).filter(Course.id == course_id).first()
    
    def get_all_courses(self) -> List[Course]:
        return self.session.query(Course).all()
    
    def update_course(self, course_id: int, course_data: CourseUpdate) -> Optional[Course]:
        course = self.get_course_by_id(course_id)
        if not course:
            return None
        
        update_data = course_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(course, field, value)
        
        self.session.commit()
        self.session.refresh(course)
        return course
    
    def delete_course(self, course_id: int) -> bool:
        course = self.get_course_by_id(course_id)
        if not course:
            return False
        
        self.session.delete(course)
        self.session.commit()
        return True

