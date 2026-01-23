"""Chatbot routes for v1 API."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from src.controllers.chatbot_controller import ChatbotController
from src.container import get_container

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    conversation_history: Optional[List[Dict]] = []


def get_chatbot_controller() -> ChatbotController:
    """Dependency to get chatbot controller."""
    container = get_container()
    chatbot_service = container.get('chatbot_service')
    return ChatbotController(chatbot_service)


@router.post("/chatbot/chat")
async def chat(
    request: ChatRequest,
    controller: ChatbotController = Depends(get_chatbot_controller)
):
    """Chatbot chat endpoint."""
    return controller.handle_chat(request.message, request.conversation_history)
