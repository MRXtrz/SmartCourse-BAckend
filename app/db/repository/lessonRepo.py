from .base import BaseRepository
from app.db.models.lesson import Lesson
from app.db.schemas.lesson import LessonCreate, LessonUpdate
from typing import List, Optional


class LessonRepository(BaseRepository):
    def create_lesson(self, lesson_data: LessonCreate) -> Lesson:
        new_lesson = Lesson(**lesson_data.model_dump())
        self.session.add(new_lesson)
        self.session.commit()
        self.session.refresh(new_lesson)
        return new_lesson
    
    def get_lesson_by_id(self, lesson_id: int) -> Optional[Lesson]:
        return self.session.query(Lesson).filter(Lesson.id == lesson_id).first()
    
    def get_lessons_by_course_id(self, course_id: int) -> List[Lesson]:
        return self.session.query(Lesson).filter(Lesson.course_id == course_id).all()
    
    def update_lesson(self, lesson_id: int, lesson_data: LessonUpdate) -> Optional[Lesson]:
        lesson = self.get_lesson_by_id(lesson_id)
        if not lesson:
            return None
        
        update_data = lesson_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lesson, field, value)
        
        self.session.commit()
        self.session.refresh(lesson)
        return lesson
    
    def delete_lesson(self, lesson_id: int) -> bool:
        lesson = self.get_lesson_by_id(lesson_id)
        if not lesson:
            return False
        
        self.session.delete(lesson)
        self.session.commit()
        return True
    
    def count_lessons_by_course_id(self, course_id: int) -> int:
        return self.session.query(Lesson).filter(Lesson.course_id == course_id).count()

