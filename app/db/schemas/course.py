from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class CourseOutput(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CourseWithProgress(CourseOutput):
    progress_percentage: float
    total_lessons: int
    completed_lessons: int


class CourseWithLessons(CourseOutput):
    lessons: List["LessonOutput"] = []


from app.db.schemas.lesson import LessonOutput
CourseWithLessons.model_rebuild()


class CourseOutputSimple(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

