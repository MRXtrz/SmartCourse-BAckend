from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AssignmentBase(BaseModel):
    title: str
    description: str
    instructions: str


class AssignmentCreate(AssignmentBase):
    lesson_id: int


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None


class AssignmentOutput(AssignmentBase):
    id: int
    lesson_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AssignmentSubmissionCreate(BaseModel):
    assignment_id: int
    answer: str


class AssignmentSubmissionOutput(BaseModel):
    id: int
    assignment_id: int
    user_id: int
    answer: str
    completed: bool
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AssignmentWithSubmission(AssignmentOutput):
    submission: Optional[AssignmentSubmissionOutput] = None

