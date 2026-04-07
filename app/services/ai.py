"""
AI service for interacting with Google's Gemini API.
Handles conversation context and generates AI responses.
"""

import google.generativeai as genai
from typing import List, Dict, Optional
from app.config import settings


class AIService:
    """
    Service for interacting with Google's Gemini AI model.
    
    This service manages the connection to the Gemini API and generates
    responses based on conversation history.
    
    Attributes:
        model: The Gemini generative model instance
        system_prompt: Base instruction prompt for the AI
    """
    
    def __init__(self):
        """
        Initialize the Gemini AI service with API key from settings.
        
        Raises:
            ValueError: If GEMINI_API_KEY is not configured
        """
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found in configuration. "
                "Please add it to your .env file."
            )
        
        # Configure the Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        # Initialize the model with the configured model name
        self.model = genai.GenerativeModel(settings.LLM_MODEL)
        
        # System prompt to guide AI behavior
        self.system_prompt = (
            "You are a helpful, friendly, and knowledgeable AI assistant. "
            "You remember previous messages in the conversation and provide "
            "contextually relevant responses. Be concise but informative. "
            "If you don't know something, say so honestly. "
            "Be respectful and professional in all interactions."
        )
        
        print(f"AI Service initialized with model: {settings.LLM_MODEL}")
    
    def get_response(self, history: List[Dict[str, str]], user_message: str) -> str:
        """
        Generate an AI response based on conversation history.
        
        Args:
            history: List of previous messages with 'role' and 'content' keys
            user_message: Current user message to respond to
            
        Returns:
            AI-generated response text, or error message if generation fails
        """
        try:
            # Start a new chat session
            chat = self.model.start_chat(history=[])
            
            # Send system prompt to establish behavior
            chat.send_message(self.system_prompt)
            
            # Send all previous user messages to establish context
            for message in history:
                if message.get("role") == "user":
                    content = message.get("content", "")
                    if content and content.strip():
                        chat.send_message(content)
            
            # Send the current user message and get response
            response = chat.send_message(user_message)
            
            # Return the response text
            return response.text
        
        except Exception as exception:
            error_message = f"AI Service Error: {str(exception)}"
            print(error_message)
            
            # Provide user-friendly error message
            if "API key" in str(exception).lower():
                return (
                    "I'm having trouble authenticating with the AI service. "
                    "Please check that your API key is configured correctly."
                )
            elif "model" in str(exception).lower():
                return (
                    "I'm having trouble with the AI model configuration. "
                    "Please check that the model name is correct."
                )
            else:
                return (
                    f"I encountered an error while processing your request. "
                    f"Please try again later. Error: {str(exception)[:100]}"
                )
    
    def test_connection(self) -> bool:
        """
        Test if the Gemini API connection is working properly.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Try to generate a simple response
            response = self.model.generate_content("Reply with 'OK'")
            return response is not None and len(response.text) > 0
        except Exception as exception:
            print(f"Connection test failed: {exception}")
            return False
    
    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the currently configured model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": settings.LLM_MODEL,
            "api_configured": bool(settings.GEMINI_API_KEY),
            "status": "connected" if self.test_connection() else "disconnected"
        }