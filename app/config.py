"""
Configuration management for the AI Chatbot application.
Loads environment variables and provides settings for the application.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Application settings loaded from environment variables.
    
    Attributes:
        GEMINI_API_KEY: API key for Google Gemini AI service
        LLM_MODEL: Model name for the language model
        HOST: Host address to bind the server
        PORT: Port number to bind the server
        MAX_HISTORY_LENGTH: Maximum number of messages to keep per session
    """
    
    def __init__(self):
        self.GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
        self.LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-pro")
        self.HOST: str = os.getenv("HOST", "0.0.0.0")
        self.PORT: int = int(os.getenv("PORT", "8000"))
        self.MAX_HISTORY_LENGTH: int = int(os.getenv("MAX_HISTORY_LENGTH", "50"))
    
    def validate(self) -> bool:
        """
        Validate that required settings are present.
        
        Returns:
            True if all required settings are valid, False otherwise.
        """
        if not self.GEMINI_API_KEY:
            print("ERROR: GEMINI_API_KEY is not set in .env file")
            return False
        if self.GEMINI_API_KEY == "your_gemini_api_key_here":
            print("ERROR: Please replace the placeholder API key with your actual Gemini API key")
            return False
        return True

# Create global settings instance
settings = Settings()

# Validate on import
if not settings.validate():
    print("Application may not function correctly. Please fix the configuration.")