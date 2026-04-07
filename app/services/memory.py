"""
Memory service for managing conversation sessions and history.
Provides thread-safe storage and retrieval of chat messages per session.
"""

from typing import Dict, List, Optional
from datetime import datetime
import threading
import uuid


class MemoryService:
    """
    In-memory session management for chat history.
    
    This service stores conversation history for multiple sessions
    with thread-safe operations for concurrent access.
    
    Attributes:
        sessions: Dictionary mapping session_id to list of messages
        _lock: Thread lock for safe concurrent access
    """
    
    def __init__(self):
        """Initialize empty session storage with thread lock."""
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        self._lock = threading.Lock()
        self._creation_times: Dict[str, datetime] = {}
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """
        Create a new session with optional custom ID.
        
        Args:
            session_id: Optional custom session ID. If not provided, generates UUID.
            
        Returns:
            The session ID for the new session
        """
        with self._lock:
            if session_id is None:
                session_id = str(uuid.uuid4())
            
            if session_id not in self.sessions:
                self.sessions[session_id] = []
                self._creation_times[session_id] = datetime.now()
            
            return session_id
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """
        Add a message to a session's history.
        
        Args:
            session_id: Unique identifier for the session
            role: Either 'user' or 'assistant'
            content: Message content text
            
        Raises:
            ValueError: If session_id is empty or role is invalid
        """
        if not session_id or not session_id.strip():
            raise ValueError("session_id cannot be empty")
        
        if role not in ['user', 'assistant']:
            raise ValueError("role must be either 'user' or 'assistant'")
        
        if not content or not content.strip():
            raise ValueError("content cannot be empty")
        
        with self._lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = []
                self._creation_times[session_id] = datetime.now()
            
            self.sessions[session_id].append({
                "role": role,
                "content": content
            })
    
    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Retrieve full conversation history for a session.
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            List of messages in chronological order, or empty list if session not found
        """
        if not session_id or not session_id.strip():
            return []
        
        with self._lock:
            return self.sessions.get(session_id, []).copy()
    
    def get_last_n_messages(self, session_id: str, n: int) -> List[Dict[str, str]]:
        """
        Retrieve the last N messages from a session.
        
        Args:
            session_id: Unique identifier for the session
            n: Number of recent messages to retrieve
            
        Returns:
            List of the N most recent messages
        """
        history = self.get_history(session_id)
        return history[-n:] if history else []
    
    def clear_history(self, session_id: str) -> bool:
        """
        Clear all messages for a session but keep the session.
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            True if session existed and was cleared, False otherwise
        """
        if not session_id or not session_id.strip():
            return False
        
        with self._lock:
            if session_id in self.sessions:
                self.sessions[session_id] = []
                return True
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Completely remove a session and all its history.
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            True if session existed and was deleted, False otherwise
        """
        if not session_id or not session_id.strip():
            return False
        
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                if session_id in self._creation_times:
                    del self._creation_times[session_id]
                return True
            return False
    
    def get_all_sessions(self) -> List[str]:
        """
        Get list of all active session IDs.
        
        Returns:
            List of all session IDs currently in memory
        """
        with self._lock:
            return list(self.sessions.keys())
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """
        Get information about a session.
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            Dictionary with session info or None if not found
        """
        with self._lock:
            if session_id in self.sessions:
                return {
                    "session_id": session_id,
                    "message_count": len(self.sessions[session_id]),
                    "created_at": self._creation_times.get(session_id),
                    "has_messages": len(self.sessions[session_id]) > 0
                }
            return None
    
    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            True if session exists, False otherwise
        """
        with self._lock:
            return session_id in self.sessions