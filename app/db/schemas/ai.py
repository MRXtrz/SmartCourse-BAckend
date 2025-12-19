from pydantic import BaseModel
from typing import Optional


class AIChatRequest(BaseModel):
    course_title: str
    lesson_title: str
    question: str


class AIChatResponse(BaseModel):
    answer: str


class AIAssignmentCheckRequest(BaseModel):
    course_title: str
    lesson_title: str
    assignment_title: str
    assignment_instructions: str
    user_answer: str


class AIAssignmentCheckResponse(BaseModel):
    is_correct: bool
    explanation: str
    suggested_answer: Optional[str] = None

