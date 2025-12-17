from .base import BaseRepository
from app.db.models.progress import Progress
from app.db.schemas.progress import ProgressCreate
from typing import List, Optional
from datetime import datetime


class ProgressRepository(BaseRepository):
    def create_or_update_progress(self, user_id: int, lesson_id: int, course_id: int, completed: bool) -> Progress:
        progress = self.session.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.lesson_id == lesson_id
        ).first()
        
        if progress:
            progress.completed = completed
            progress.course_id = course_id
            if completed:
                progress.completed_at = datetime.utcnow()
            else:
                progress.completed_at = None
            self.session.commit()
            self.session.refresh(progress)
            return progress
        else:
            new_progress = Progress(
                user_id=user_id,
                lesson_id=lesson_id,
                course_id=course_id,
                completed=completed,
                completed_at=datetime.utcnow() if completed else None
            )
            self.session.add(new_progress)
            self.session.commit()
            self.session.refresh(new_progress)
            return new_progress
    
    def get_progress_by_user_and_lesson(self, user_id: int, lesson_id: int) -> Optional[Progress]:
        return self.session.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.lesson_id == lesson_id
        ).first()
    
    def get_user_progress_by_course(self, user_id: int, course_id: int) -> List[Progress]:
        return self.session.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.course_id == course_id
        ).all()
    
    def get_all_user_progress(self, user_id: int) -> List[Progress]:
        return self.session.query(Progress).filter(Progress.user_id == user_id).all()
    
    def count_completed_lessons_by_course(self, user_id: int, course_id: int) -> int:
        return self.session.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.course_id == course_id,
            Progress.completed == True
        ).count()

