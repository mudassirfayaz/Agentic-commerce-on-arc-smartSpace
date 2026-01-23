"""
Chatbot API endpoint for SmartSpace landing page.
Handles Gemini API integration with SmartSpace.md as context.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Chatbot will use mock responses.")


class ChatbotService:
    """Service for handling chatbot requests with Gemini API and SmartSpace.md context."""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.smartspace_doc_path = os.getenv(
            "SMARTSPACE_DOC_PATH",
            str(Path(__file__).parent.parent.parent / "openspec" / "SmartSpace.md")
        )
        self.smartspace_content = None
        self.model = None
        
        if GEMINI_AVAILABLE and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            print("Warning: Gemini API not configured. Using mock responses.")
    
    def _load_smartspace_doc(self) -> str:
        """Load SmartSpace.md content as the primary context source."""
        if self.smartspace_content:
            return self.smartspace_content
        
        try:
            doc_path = Path(self.smartspace_doc_path)
            if doc_path.exists():
                with open(doc_path, 'r', encoding='utf-8') as f:
                    self.smartspace_content = f.read()
                return self.smartspace_content
            else:
                print(f"Warning: SmartSpace.md not found at {doc_path}")
                return "SmartSpace documentation not available."
        except Exception as e:
            print(f"Error loading SmartSpace.md: {e}")
            return "Error loading SmartSpace documentation."
    
    def _build_prompt(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Build the prompt with SmartSpace.md as context."""
        smartspace_doc = self._load_smartspace_doc()
        
        # Build context from conversation history
        history_context = ""
        if conversation_history:
            history_context = "\n\nPrevious conversation:\n"
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_context += f"{role}: {msg.get('content', '')}\n"
        
        prompt = f"""You are a helpful assistant for SmartSpace, an autonomous pay-per-use API access gateway with USDC payments.

SmartSpace Documentation (Primary Context Source):
{smartspace_doc}
{history_context}

User Question: {user_message}

Please provide a helpful response based on the SmartSpace documentation above. If the question is not directly answered in the documentation, provide the most relevant information you can find, or politely indicate that the information is not available in the documentation."""
        
        return prompt
    
    def get_response(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Get response from Gemini API with SmartSpace.md context."""
        if not self.model:
            # Mock response for development
            return "I'm here to help with SmartSpace! However, the Gemini API is not configured. Please set GEMINI_API_KEY environment variable to enable full functionality."
        
        try:
            prompt = self._build_prompt(user_message, conversation_history)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."


# Global service instance
_chatbot_service = None

def get_chatbot_service() -> ChatbotService:
    """Get or create chatbot service instance."""
    global _chatbot_service
    if _chatbot_service is None:
        _chatbot_service = ChatbotService()
    return _chatbot_service


def handle_chatbot_request(data: Dict) -> Dict:
    """
    Handle chatbot API request.
    
    Args:
        data: Request data with 'message' and optional 'conversation_history'
    
    Returns:
        Dict with 'response' field
    """
    service = get_chatbot_service()
    
    user_message = data.get("message", "")
    conversation_history = data.get("conversation_history", [])
    
    if not user_message:
        return {"error": "Message is required"}, 400
    
    response = service.get_response(user_message, conversation_history)
    
    return {"response": response}

