"""
Chat API route handlers for the AI chatbot.
Provides endpoints for conversation, history management, and health checks.
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from app.models.schemas import (
    ChatRequest, 
    ChatResponse, 
    HistoryResponse, 
    HealthResponse
)
from app.services.memory import MemoryService
from app.services.ai import AIService

# Create router instance
router = APIRouter(prefix="/api", tags=["chat"])

# Initialize services as singletons
memory_service = MemoryService()
ai_service = AIService()


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a message to the AI chatbot",
    description="Accepts a user message and session ID, returns AI response with conversation memory."
)
async def send_message(request: ChatRequest) -> ChatResponse:
    """
    Process a user message and return an AI response.
    
    This endpoint maintains conversation memory per session. The AI will
    remember previous messages within the same session_id.
    
    Args:
        request: ChatRequest containing session_id and message
        
    Returns:
        ChatResponse containing the AI's reply
        
    Raises:
        HTTPException: If message processing fails
    """
    try:
        # Validate session_id
        if not request.session_id or not request.session_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="session_id cannot be empty"
            )
        
        # Validate message
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="message cannot be empty"
            )
        
        # Store user message in memory
        memory_service.add_message(
            session_id=request.session_id,
            role="user",
            content=request.message
        )
        
        # Retrieve conversation history
        history = memory_service.get_history(request.session_id)
        
        # Generate AI response using conversation context
        ai_response = ai_service.get_response(history, request.message)
        
        # Store AI response in memory
        memory_service.add_message(
            session_id=request.session_id,
            role="assistant",
            content=ai_response
        )
        
        return ChatResponse(
            session_id=request.session_id,
            response=ai_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.get(
    "/history/{session_id}",
    response_model=HistoryResponse,
    summary="Get conversation history",
    description="Retrieve all messages for a specific session."
)
async def get_history(session_id: str) -> HistoryResponse:
    """
    Retrieve the full conversation history for a session.
    
    Args:
        session_id: Unique identifier for the conversation session
        
    Returns:
        HistoryResponse containing all messages in the session
        
    Raises:
        HTTPException: If session not found
    """
    if not session_id or not session_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="session_id cannot be empty"
        )
    
    history = memory_service.get_history(session_id)
    
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No history found for session: {session_id}"
        )
    
    return HistoryResponse(
        session_id=session_id,
        history=history,
        total_messages=len(history)
    )


@router.delete(
    "/history/{session_id}",
    status_code=status.HTTP_200_OK,
    summary="Clear conversation history",
    description="Delete all messages for a specific session."
)
async def clear_history(session_id: str) -> Dict[str, Any]:
    """
    Clear all conversation history for a session.
    
    This resets the conversation - the AI will no longer remember
    previous messages from this session.
    
    Args:
        session_id: Unique identifier for the conversation session
        
    Returns:
        Dictionary with status message
        
    Raises:
        HTTPException: If session not found
    """
    if not session_id or not session_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="session_id cannot be empty"
        )
    
    success = memory_service.clear_history(session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}"
        )
    
    return {
        "status": "success",
        "message": f"History cleared for session: {session_id}",
        "session_id": session_id
    }


@router.delete(
    "/session/{session_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete session completely",
    description="Remove a session and all its history."
)
async def delete_session(session_id: str) -> Dict[str, Any]:
    """
    Completely delete a session and all its conversation history.
    
    Args:
        session_id: Unique identifier for the conversation session
        
    Returns:
        Dictionary with status message
        
    Raises:
        HTTPException: If session not found
    """
    if not session_id or not session_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="session_id cannot be empty"
        )
    
    success = memory_service.delete_session(session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session not found: {session_id}"
        )
    
    return {
        "status": "success",
        "message": f"Session deleted: {session_id}",
        "session_id": session_id
    }


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Verify the API service is running and healthy."
)
async def health_check() -> HealthResponse:
    """
    Perform a health check on the API service.
    
    Returns:
        HealthResponse indicating service status
    """
    # Check AI service connectivity
    ai_healthy = ai_service.test_connection()
    
    return HealthResponse(
        status="healthy" if ai_healthy else "degraded",
        version="1.0.0"
    )


@router.get(
    "/sessions",
    summary="List all active sessions",
    description="Get a list of all active session IDs (for debugging)."
)
async def list_sessions() -> Dict[str, Any]:
    """
    List all active sessions currently in memory.
    
    Returns:
        Dictionary with session list and count
    """
    sessions = memory_service.get_all_sessions()
    return {
        "total_active_sessions": len(sessions),
        "sessions": sessions
    }