"""
Main FastAPI application entry point for the AI Chatbot.
Configures the application, middleware, and includes all routes.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.routes import chat
from app.config import settings


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="AI Chatbot API",
        description="""
        A production-ready conversational AI chatbot with persistent memory.
        
        Features:
        - Multi-turn conversations with context memory
        - Session isolation (different users don't interfere)
        - Conversation history retrieval
        - Session management (clear/delete)
        - Automatic API documentation
        
        ## Authentication
        No authentication required for this assessment version.
        
        ## Rate Limiting
        Not implemented in this version.
        """,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_tags=[
            {
                "name": "chat",
                "description": "Chat operations - send messages and get AI responses"
            },
            {
                "name": "history",
                "description": "History management - retrieve and clear conversation history"
            },
            {
                "name": "health",
                "description": "Health checks and service monitoring"
            }
        ]
    )
    
    # Configure CORS middleware for cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=3600,
    )
    
    # Include all route handlers
    app.include_router(chat.router)
    
    # Exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        """
        Handle request validation errors.
        """
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "errors": exc.errors(),
                "body": exc.body
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """
        Handle HTTP exceptions.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """
        Handle unexpected exceptions.
        """
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "status_code": 500
            }
        )
    
    # Root endpoint
    @app.get(
        "/",
        tags=["health"],
        summary="API information",
        description="Get basic information about the API"
    )
    async def root():
        """
        Root endpoint providing API overview.
        
        Returns:
            Dictionary with API information and available endpoints
        """
        return {
            "name": "AI Chatbot API",
            "version": "1.0.0",
            "description": "Conversational AI chatbot with persistent memory",
            "documentation": "/docs",
            "interactive_docs": "/redoc",
            "health_check": "/api/health",
            "endpoints": {
                "POST /api/chat": "Send a message to the AI chatbot",
                "GET /api/history/{session_id}": "Get conversation history for a session",
                "DELETE /api/history/{session_id}": "Clear conversation history for a session",
                "DELETE /api/session/{session_id}": "Delete a session completely",
                "GET /api/health": "Check API health status",
                "GET /api/sessions": "List all active sessions (debug)"
            },
            "configuration": {
                "model": settings.LLM_MODEL,
                "host": settings.HOST,
                "port": settings.PORT
            }
        }
    
    # Startup event handler
    @app.on_event("startup")
    async def startup_event():
        """
        Execute on application startup.
        """
        print("=" * 50)
        print("AI CHATBOT API - STARTING")
        print("=" * 50)
        print(f"Server will run on: http://{settings.HOST}:{settings.PORT}")
        print(f"API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
        print(f"Alternative Docs: http://{settings.HOST}:{settings.PORT}/redoc")
        print(f"AI Model: {settings.LLM_MODEL}")
        print(f"API Key Configured: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
        print("=" * 50)
        print("Ready to accept requests")
        print("=" * 50)
    
    # Shutdown event handler
    @app.on_event("shutdown")
    async def shutdown_event():
        """
        Execute on application shutdown.
        """
        print("=" * 50)
        print("AI CHATBOT API - SHUTTING DOWN")
        print("=" * 50)
    
    return app


# Create the application instance
app = create_application()

# For direct execution
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )