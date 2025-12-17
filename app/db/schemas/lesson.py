from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LessonBase(BaseModel):
    title: str
    content: str


class LessonCreate(LessonBase):
    course_id: int


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class LessonOutput(LessonBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LessonWithProgress(LessonOutput):
    completed: bool

