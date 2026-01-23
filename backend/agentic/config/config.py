"""
Configuration Management
Loads and manages application configuration
"""
import os
from dotenv import load_dotenv


class Config:
    """Application configuration"""
    
    def __init__(self):
        """Load configuration from environment"""
        load_dotenv()
        
       
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        
        self.backend_api_url = os.getenv("BACKEND_API_URL", "")
        self.smartspace_gateway_url = os.getenv("SMARTSPACE_GATEWAY_URL", "")
    
    def validate(self):
        """Validate required configuration"""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required")
        return True

# Global config instance
config = Config()

