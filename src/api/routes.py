"""API routes for the AI-Powered Interactive Coding Tutor."""
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, validator
from src.services.tutor_service import TutorService

logger = logging.getLogger(__name__)
router = APIRouter()

# Request and Response Models
class AskRequest(BaseModel):
    """Request model for asking questions."""
    question: str = Field(..., min_length=1, max_length=2000, description="The question to ask")
    user_id: Optional[str] = Field(None, description="Optional user ID for session tracking")
    use_history: bool = Field(True, description="Whether to use conversation history")
    
    @validator('question')
    def question_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Question cannot be empty')
        return v.strip()


class AskResponse(BaseModel):
    """Response model for question answers."""
    answer: str = Field(..., description="AI-generated answer")
    user_id: Optional[str] = Field(None, description="User ID if provided")


class SubmitCodeRequest(BaseModel):
    """Request model for code submission."""
    code: str = Field(..., min_length=1, max_length=10000, description="The code to analyze")
    language: str = Field(..., min_length=1, max_length=50, description="Programming language")
    context: Optional[str] = Field(None, max_length=500, description="Optional context about the code")
    user_id: Optional[str] = Field(None, description="Optional user ID for tracking")
    
    @validator('code')
    def code_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Code cannot be empty')
        return v.strip()
    
    @validator('language')
    def language_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Language cannot be empty')
        return v.strip()


class SubmitCodeResponse(BaseModel):
    """Response model for code feedback."""
    feedback: str = Field(..., description="AI-generated code feedback")
    user_id: Optional[str] = Field(None, description="User ID if provided")


class ClearSessionRequest(BaseModel):
    """Request model for clearing session."""
    user_id: str = Field(..., min_length=1, description="User ID")


class SessionSummaryResponse(BaseModel):
    """Response model for session summary."""
    user_id: str
    total_questions: int
    total_code_submissions: int
    has_active_session: bool


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    message: str


# Initialize the service
tutor_service = TutorService()


@router.get("/api/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return HealthResponse(
        status="healthy",
        message="AI-Powered Interactive Coding Tutor is running"
    )


@router.post(
    "/api/ask", 
    response_model=AskResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tutoring"],
    summary="Ask a coding question",
    description="Submit a coding question and receive an AI-powered answer. Optionally provide user_id for conversation history."
)
def ask_question(request: AskRequest):
    """
    Ask a coding question and receive an AI-generated answer.
    
    - **question**: The coding question to ask (required)
    - **user_id**: Optional user ID for session tracking and conversation history
    - **use_history**: Whether to use previous conversation context (default: true)
    """
    try:
        logger.info(f"Received question request from user: {request.user_id}")
        answer = tutor_service.answer_question(
            request.question,
            request.user_id,
            request.use_history
        )
        return AskResponse(answer=answer, user_id=request.user_id)
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process question: {str(e)}"
        )


@router.post(
    "/api/submit_code",
    response_model=SubmitCodeResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tutoring"],
    summary="Submit code for review",
    description="Submit code for AI-powered analysis and feedback."
)
def submit_code(request: SubmitCodeRequest):
    """
    Submit code for analysis and receive detailed feedback.
    
    - **code**: The code to analyze (required)
    - **language**: Programming language (required)
    - **context**: Optional description of what the code should do
    - **user_id**: Optional user ID for tracking submissions
    """
    try:
        logger.info(f"Received code submission ({request.language}) from user: {request.user_id}")
        feedback = tutor_service.provide_code_feedback(
            request.code,
            request.language,
            request.context,
            request.user_id
        )
        return SubmitCodeResponse(feedback=feedback, user_id=request.user_id)
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze code: {str(e)}"
        )


@router.post(
    "/api/session/clear",
    status_code=status.HTTP_200_OK,
    tags=["Session"],
    summary="Clear user session",
    description="Clear all session data for a specific user."
)
def clear_session(request: ClearSessionRequest):
    """
    Clear the session data for a user.
    
    - **user_id**: User ID whose session should be cleared
    """
    try:
        logger.info(f"Clearing session for user: {request.user_id}")
        tutor_service.clear_session(request.user_id)
        return {"message": f"Session cleared for user {request.user_id}"}
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear session: {str(e)}"
        )


@router.get(
    "/api/session/{user_id}/summary",
    response_model=SessionSummaryResponse,
    tags=["Session"],
    summary="Get session summary",
    description="Retrieve session statistics for a specific user."
)
def get_session_summary(user_id: str):
    """
    Get a summary of the user's session.
    
    - **user_id**: User ID to get summary for
    """
    try:
        logger.info(f"Getting session summary for user: {user_id}")
        summary = tutor_service.get_session_summary(user_id)
        return SessionSummaryResponse(user_id=user_id, **summary)
    except Exception as e:
        logger.error(f"Error getting session summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session summary: {str(e)}"
        )
