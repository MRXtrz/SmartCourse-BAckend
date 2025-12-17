from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security.authHandler import get_current_user, get_current_admin_user
from app.db.models.user import User
from app.db.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentOutput, AssignmentWithSubmission, AssignmentSubmissionCreate
from app.service.assignmentService import AssignmentService
from pydantic import BaseModel

assignmentsRouter = APIRouter()


class SubmitAssignmentRequest(BaseModel):
    answer: str


@assignmentsRouter.get("/lessons/{lesson_id}/assignments", response_model=List[AssignmentWithSubmission])
async def get_assignments_by_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assignment_service = AssignmentService(db)
    return assignment_service.get_assignments_by_lesson_id(lesson_id, current_user)


@assignmentsRouter.get("/{assignment_id}", response_model=AssignmentOutput)
async def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment_service = AssignmentService(db)
    return assignment_service.get_assignment_by_id(assignment_id)


@assignmentsRouter.post("", response_model=AssignmentOutput, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    assignment_service = AssignmentService(db)
    return assignment_service.create_assignment(assignment_data)


@assignmentsRouter.post("/{assignment_id}/submit", status_code=status.HTTP_200_OK)
async def submit_assignment(
    assignment_id: int,
    request: SubmitAssignmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.db.schemas.assignment import AssignmentSubmissionOutput
    assignment_service = AssignmentService(db)
    submission = assignment_service.submit_assignment(assignment_id, request.answer, current_user)
    return AssignmentSubmissionOutput(
        id=submission.id,
        assignment_id=submission.assignment_id,
        user_id=submission.user_id,
        answer=submission.answer,
        completed=submission.completed,
        completed_at=submission.completed_at,
        created_at=submission.created_at,
        updated_at=submission.updated_at
    )


@assignmentsRouter.put("/{assignment_id}", response_model=AssignmentOutput)
async def update_assignment(
    assignment_id: int,
    assignment_data: AssignmentUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    assignment_service = AssignmentService(db)
    return assignment_service.update_assignment(assignment_id, assignment_data)


@assignmentsRouter.delete("/{assignment_id}", status_code=status.HTTP_200_OK)
async def delete_assignment(
    assignment_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    assignment_service = AssignmentService(db)
    return assignment_service.delete_assignment(assignment_id)

