from decouple import config
from openai import OpenAI
from app.db.schemas.ai import AIChatRequest, AIChatResponse
from fastapi import HTTPException, status


class AIService:
    def __init__(self):
        api_key = config("OPENAI_API_KEY", default="")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def chat(self, request: AIChatRequest) -> AIChatResponse:
        prompt = f"""You are an AI tutor on an online course platform.

Your task:
- Explain concepts clearly and simply
- Help students understand the lesson

Course: {request.course_title}
Lesson: {request.lesson_title}

Rules:
- Act like a teacher
- Use simple examples
- be communicative
- always

Student question:
{request.question}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI tutor for an online learning platform."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            return AIChatResponse(answer=answer)
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error communicating with AI service: {str(e)}"
            )

