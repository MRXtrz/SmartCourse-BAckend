from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProgressBase(BaseModel):
    lesson_id: int
    completed: bool = False


class ProgressCreate(ProgressBase):
    pass


class ProgressUpdate(BaseModel):
    completed: Optional[bool] = None


class ProgressOutput(ProgressBase):
    id: int
    user_id: int
    course_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProgressSummary(BaseModel):
    course_id: int
    course_title: str
    total_lessons: int
    completed_lessons: int
    progress_percentage: float

