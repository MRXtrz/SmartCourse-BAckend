from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security.authHandler import get_current_user
from app.db.models.user import User
from app.db.schemas.ai import AIChatRequest, AIChatResponse
from app.service.aiService import AIService

aiRouter = APIRouter()


@aiRouter.post("/chat", response_model=AIChatResponse)
async def chat_with_ai(
    request: AIChatRequest,
    current_user: User = Depends(get_current_user)
):
    ai_service = AIService()
    return ai_service.chat(request)

