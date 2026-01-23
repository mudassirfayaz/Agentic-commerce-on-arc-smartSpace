"""Chatbot controller."""

from typing import List, Dict
from src.services.chatbot import ChatbotService
from src.utils.responses import success_response, error_response
from src.utils.exceptions import ValidationError


class ChatbotController:
    """Controller for chatbot endpoints."""
    
    def __init__(self, chatbot_service: ChatbotService):
        """
        Initialize chatbot controller.
        
        Args:
            chatbot_service: Chatbot service instance
        """
        self.chatbot_service = chatbot_service
    
    def handle_chat(self, message: str, conversation_history: List[Dict] = None):
        """
        Handle chatbot chat request.
        
        Args:
            message: User message
            conversation_history: Optional conversation history
            
        Returns:
            Response dictionary
        """
        try:
            if not message:
                return error_response(
                    message="Message is required",
                    status_code=400
                )
            
            if conversation_history is None:
                conversation_history = []
            
            response = self.chatbot_service.get_response(message, conversation_history)
            
            return success_response(
                data={"response": response},
                message="Chat response generated"
            )
        except ValidationError as e:
            return error_response(
                message=e.message,
                status_code=e.status_code,
                details=e.details
            )
        except Exception as e:
            return error_response(
                message=f"Error processing chat request: {str(e)}",
                status_code=500
            )
