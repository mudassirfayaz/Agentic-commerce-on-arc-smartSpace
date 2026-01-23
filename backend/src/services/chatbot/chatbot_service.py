"""
Chatbot service for SmartSpace.
Migrated from backend/src/chatbot.py
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not installed. Chatbot will use mock responses.")


class ChatbotService:
    """Service for handling chatbot requests with Gemini API and SmartSpace.md context."""
    
    def __init__(self, gemini_api_key: Optional[str] = None, smartspace_doc_path: Optional[str] = None):
        """
        Initialize chatbot service.
        
        Args:
            gemini_api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            smartspace_doc_path: Path to SmartSpace.md (defaults to env var or default path)
        """
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.smartspace_doc_path = smartspace_doc_path or os.getenv(
            "SMARTSPACE_DOC_PATH",
            str(Path(__file__).parent.parent.parent.parent / "openspec" / "SmartSpace.md")
        )
        self.smartspace_content = None
        self.model = None
        
        if GEMINI_AVAILABLE and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            logger.warning("Gemini API not configured. Using mock responses.")
    
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
                logger.warning(f"SmartSpace.md not found at {doc_path}")
                return "SmartSpace documentation not available."
        except Exception as e:
            logger.error(f"Error loading SmartSpace.md: {e}")
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
    
    def get_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """
        Get response from Gemini API with SmartSpace.md context.
        
        Args:
            user_message: User's message
            conversation_history: Optional conversation history
            
        Returns:
            Response text
        """
        if conversation_history is None:
            conversation_history = []
        
        if not self.model:
            # Mock response for development
            return "I'm here to help with SmartSpace! However, the Gemini API is not configured. Please set GEMINI_API_KEY environment variable to enable full functionality."
        
        try:
            prompt = self._build_prompt(user_message, conversation_history)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."

