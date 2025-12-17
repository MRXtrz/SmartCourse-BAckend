from sqlalchemy.orm import Session
from app.db.repository.assignmentRepo import AssignmentRepository
from app.db.repository.lessonRepo import LessonRepository
from app.db.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentWithSubmission
from app.db.models.user import User
from typing import List
from fastapi import HTTPException, status


class AssignmentService:
    def __init__(self, db: Session):
        self.assignment_repo = AssignmentRepository(db)
        self.lesson_repo = LessonRepository(db)
        self.db = db
    
    def create_assignment(self, assignment_data: AssignmentCreate):
        lesson = self.lesson_repo.get_lesson_by_id(assignment_data.lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
        
        return self.assignment_repo.create_assignment(assignment_data)
    
    def get_assignment_by_id(self, assignment_id: int):
        assignment = self.assignment_repo.get_assignment_by_id(assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        return assignment
    
    def get_assignments_by_lesson_id(self, lesson_id: int, user: User = None) -> List:
        lesson = self.lesson_repo.get_lesson_by_id(lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
        
        assignments = self.assignment_repo.get_assignments_by_lesson_id(lesson_id)
        
        if user:
            result = []
            for assignment in assignments:
                submission = self.assignment_repo.get_submission_by_user_and_assignment(user.id, assignment.id)
                from app.db.schemas.assignment import AssignmentSubmissionOutput
                submission_output = None
                if submission:
                    submission_output = AssignmentSubmissionOutput(
                        id=submission.id,
                        assignment_id=submission.assignment_id,
                        user_id=submission.user_id,
                        answer=submission.answer,
                        completed=submission.completed,
                        completed_at=submission.completed_at,
                        created_at=submission.created_at,
                        updated_at=submission.updated_at
                    )
                assignment_dict = {
                    "id": assignment.id,
                    "lesson_id": assignment.lesson_id,
                    "title": assignment.title,
                    "description": assignment.description,
                    "instructions": assignment.instructions,
                    "created_at": assignment.created_at,
                    "updated_at": assignment.updated_at,
                    "submission": submission_output
                }
                result.append(AssignmentWithSubmission(**assignment_dict))
            return result
        
        return assignments
    
    def update_assignment(self, assignment_id: int, assignment_data: AssignmentUpdate):
        assignment = self.assignment_repo.update_assignment(assignment_id, assignment_data)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        return assignment
    
    def delete_assignment(self, assignment_id: int):
        if not self.assignment_repo.delete_assignment(assignment_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        return {"message": "Assignment deleted successfully"}
    
    def submit_assignment(self, assignment_id: int, answer: str, user: User):
        assignment = self.assignment_repo.get_assignment_by_id(assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        from app.db.schemas.assignment import AssignmentSubmissionCreate
        submission_data = AssignmentSubmissionCreate(
            assignment_id=assignment_id,
            answer=answer
        )
        
        return self.assignment_repo.create_submission(submission_data, user.id)

