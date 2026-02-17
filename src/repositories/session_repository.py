"""Repository for managing user session data."""
import logging
from typing import Dict, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class SessionRepository:
    """Repository for storing and retrieving user session data."""
    
    def __init__(self):
        """Initialize the session repository with in-memory storage."""
        self.sessions: Dict[str, Dict] = {}
        logger.info("SessionRepository initialized")

    def save_session(self, user_id: str, data: dict) -> None:
        """
        Save user session data.
        
        Args:
            user_id: Unique identifier for the user
            data: Session data to store
        """
        if not user_id:
            raise ValueError("user_id cannot be empty")
        
        data["last_updated"] = datetime.now(timezone.utc).isoformat()
        self.sessions[user_id] = data
        logger.debug(f"Saved session for user: {user_id}")

    def get_session(self, user_id: str) -> dict:
        """
        Retrieve user session data.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Session data dictionary, or empty dict if no session exists
        """
        if not user_id:
            raise ValueError("user_id cannot be empty")
        
        session = self.sessions.get(user_id, {})
        logger.debug(f"Retrieved session for user: {user_id}")
        return session
    
    def delete_session(self, user_id: str) -> bool:
        """
        Delete a user's session.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            True if session was deleted, False if it didn't exist
        """
        if user_id in self.sessions:
            del self.sessions[user_id]
            logger.info(f"Deleted session for user: {user_id}")
            return True
        return False
    
    def session_exists(self, user_id: str) -> bool:
        """
        Check if a session exists for a user.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            True if session exists, False otherwise
        """
        return user_id in self.sessions
