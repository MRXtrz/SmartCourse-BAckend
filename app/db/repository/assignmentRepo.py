from .base import BaseRepository
from app.db.models.assignment import Assignment, AssignmentSubmission
from app.db.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentSubmissionCreate
from typing import List, Optional
from datetime import datetime


class AssignmentRepository(BaseRepository):
    def create_assignment(self, assignment_data: AssignmentCreate) -> Assignment:
        new_assignment = Assignment(**assignment_data.model_dump())
        self.session.add(new_assignment)
        self.session.commit()
        self.session.refresh(new_assignment)
        return new_assignment
    
    def get_assignment_by_id(self, assignment_id: int) -> Optional[Assignment]:
        return self.session.query(Assignment).filter(Assignment.id == assignment_id).first()
    
    def get_assignments_by_lesson_id(self, lesson_id: int) -> List[Assignment]:
        return self.session.query(Assignment).filter(Assignment.lesson_id == lesson_id).all()
    
    def update_assignment(self, assignment_id: int, assignment_data: AssignmentUpdate) -> Optional[Assignment]:
        assignment = self.get_assignment_by_id(assignment_id)
        if not assignment:
            return None
        
        update_data = assignment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(assignment, field, value)
        
        self.session.commit()
        self.session.refresh(assignment)
        return assignment
    
    def delete_assignment(self, assignment_id: int) -> bool:
        assignment = self.get_assignment_by_id(assignment_id)
        if not assignment:
            return False
        
        self.session.delete(assignment)
        self.session.commit()
        return True
    
    def create_submission(self, submission_data: AssignmentSubmissionCreate, user_id: int) -> AssignmentSubmission:
        submission = AssignmentSubmission(
            assignment_id=submission_data.assignment_id,
            user_id=user_id,
            answer=submission_data.answer,
            completed=True,
            completed_at=datetime.utcnow()
        )
        self.session.add(submission)
        self.session.commit()
        self.session.refresh(submission)
        return submission
    
    def get_submission_by_user_and_assignment(self, user_id: int, assignment_id: int) -> Optional[AssignmentSubmission]:
        return self.session.query(AssignmentSubmission).filter(
            AssignmentSubmission.user_id == user_id,
            AssignmentSubmission.assignment_id == assignment_id
        ).first()
    
    def get_submissions_by_user(self, user_id: int) -> List[AssignmentSubmission]:
        return self.session.query(AssignmentSubmission).filter(
            AssignmentSubmission.user_id == user_id
        ).all()

