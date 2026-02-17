"""Service layer for tutoring functionality."""
import logging
from typing import List, Dict, Optional
from src.core.engine import AIEngine
from src.repositories.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class TutorService:
    """Service for handling tutoring requests and managing conversations."""
    
    def __init__(self):
        """Initialize the TutorService with AI engine and session repository."""
        self.ai_engine = AIEngine()
        self.session_repo = SessionRepository()
        logger.info("TutorService initialized")

    def answer_question(
        self, 
        question: str, 
        user_id: Optional[str] = None,
        use_history: bool = True
    ) -> str:
        """
        Process a user's question and return an AI-generated answer.
        
        Args:
            question: The user's question
            user_id: Optional user ID for session tracking
            use_history: Whether to use conversation history for context
            
        Returns:
            AI-generated answer
        """
        logger.info(f"Processing question from user: {user_id}")
        
        conversation_history = None
        
        # Retrieve conversation history if user_id is provided and history is enabled
        if user_id and use_history:
            session_data = self.session_repo.get_session(user_id)
            conversation_history = session_data.get("conversation_history", [])
        
        # Generate answer
        answer = self.ai_engine.generate_answer(question, conversation_history)
        
        # Save conversation to session if user_id is provided
        if user_id:
            self._update_conversation_history(user_id, question, answer)
        
        return answer
    
    def provide_code_feedback(
        self, 
        code: str, 
        language: str,
        context: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> str:
        """
        Analyze submitted code and provide feedback.
        
        Args:
            code: The code to analyze
            language: Programming language
            context: Optional context about what the code should do
            user_id: Optional user ID for tracking
            
        Returns:
            Detailed feedback about the code
        """
        logger.info(f"Providing feedback for {language} code from user: {user_id}")
        
        feedback = self.ai_engine.analyze_code(code, language, context)
        
        # Save code submission to session if user_id is provided
        if user_id:
            session_data = self.session_repo.get_session(user_id)
            submissions = session_data.get("code_submissions", [])
            submissions.append({
                "code": code,
                "language": language,
                "context": context,
                "feedback": feedback
            })
            session_data["code_submissions"] = submissions
            self.session_repo.save_session(user_id, session_data)
        
        return feedback
    
    def _update_conversation_history(self, user_id: str, question: str, answer: str) -> None:
        """
        Update the conversation history for a user session.
        
        Args:
            user_id: User identifier
            question: User's question
            answer: AI's answer
        """
        session_data = self.session_repo.get_session(user_id)
        conversation_history = session_data.get("conversation_history", [])
        
        # Add new messages to history
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": answer})
        
        # Keep only last 10 messages (5 exchanges) to avoid token limits
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        
        session_data["conversation_history"] = conversation_history
        self.session_repo.save_session(user_id, session_data)
        logger.info(f"Updated conversation history for user: {user_id}")
    
    def clear_session(self, user_id: str) -> None:
        """
        Clear the session data for a user.
        
        Args:
            user_id: User identifier
        """
        self.session_repo.save_session(user_id, {})
        logger.info(f"Cleared session for user: {user_id}")
    
    def get_session_summary(self, user_id: str) -> Dict:
        """
        Get a summary of the user's session.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with session statistics
        """
        session_data = self.session_repo.get_session(user_id)
        conversation_history = session_data.get("conversation_history", [])
        code_submissions = session_data.get("code_submissions", [])
        
        return {
            "total_questions": len([m for m in conversation_history if m.get("role") == "user"]),
            "total_code_submissions": len(code_submissions),
            "has_active_session": len(session_data) > 0
        }
