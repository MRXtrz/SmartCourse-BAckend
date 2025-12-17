from pydantic import BaseModel


class AIChatRequest(BaseModel):
    course_title: str
    lesson_title: str
    question: str


class AIChatResponse(BaseModel):
    answer: str

