"""
Pydantic schemas for API request and response validation.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Request model for the chat endpoint.
    
    Attributes:
        session_id: Unique identifier for the conversation session
        message: User's message to send to the AI
    """
    
    session_id: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Unique session identifier for conversation memory"
    )
    message: str = Field(
        ..., 
        min_length=1, 
        max_length=5000,
        description="User message content"
    )
    
    @validator('session_id')
    def validate_session_id(cls, v):
        """Ensure session_id contains only valid characters."""
        if not v.strip():
            raise ValueError('session_id cannot be empty or whitespace')
        return v.strip()
    
    @validator('message')
    def validate_message(cls, v):
        """Ensure message is not empty."""
        if not v.strip():
            raise ValueError('message cannot be empty or whitespace')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "user_session_123",
                "message": "Hello, how are you?"
            }
        }


class ChatResponse(BaseModel):
    """
    Response model for the chat endpoint.
    
    Attributes:
        session_id: The session identifier
        response: AI-generated response message
        timestamp: UTC timestamp of the response
    """
    
    session_id: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "user_session_123",
                "response": "Hello! I'm doing well, thank you for asking.",
                "timestamp": "2024-01-15T10:30:00.123456"
            }
        }


class Message(BaseModel):
    """
    Individual message in conversation history.
    
    Attributes:
        role: Either 'user' or 'assistant'
        content: Message content text
        timestamp: When the message was created
    """
    
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class HistoryResponse(BaseModel):
    """
    Response model for conversation history endpoint.
    
    Attributes:
        session_id: The session identifier
        history: List of messages in chronological order
        total_messages: Total number of messages in the session
    """
    
    session_id: str
    history: List[Dict[str, str]]
    total_messages: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "user_session_123",
                "history": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!"}
                ],
                "total_messages": 2
            }
        }


class HealthResponse(BaseModel):
    """
    Health check response model.
    
    Attributes:
        status: Service status ('healthy' or 'degraded')
        version: API version
        timestamp: When the health check was performed
    """
    
    status: str
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00.123456"
            }
        }


class ErrorResponse(BaseModel):
    """
    Error response model for API errors.
    
    Attributes:
        detail: Error description
        status_code: HTTP status code
        timestamp: When the error occurred
    """
    
    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.now)