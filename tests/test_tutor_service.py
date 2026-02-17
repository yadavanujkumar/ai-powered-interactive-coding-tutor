"""Tests for tutor service."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.tutor_service import TutorService
from src.core.engine import AIEngine
from src.repositories.session_repository import SessionRepository


@pytest.fixture
def mock_ai_engine():
    """Create a mock AI engine."""
    with patch('src.services.tutor_service.AIEngine') as mock:
        engine = mock.return_value
        engine.generate_answer.return_value = "This is a mocked answer"
        engine.analyze_code.return_value = "This is mocked feedback"
        yield engine


@pytest.fixture
def tutor_service(mock_ai_engine):
    """Create a tutor service with mocked AI engine."""
    return TutorService()


def test_answer_question_basic(tutor_service, mock_ai_engine):
    """Test basic question answering without session."""
    question = "What is a Python list?"
    answer = tutor_service.answer_question(question)
    
    assert isinstance(answer, str)
    assert len(answer) > 0
    assert answer == "This is a mocked answer"
    mock_ai_engine.generate_answer.assert_called_once()


def test_answer_question_with_user_id(tutor_service, mock_ai_engine):
    """Test question answering with user session tracking."""
    question = "What is a Python list?"
    user_id = "test_user"
    
    answer = tutor_service.answer_question(question, user_id=user_id)
    
    assert isinstance(answer, str)
    assert len(answer) > 0
    
    # Verify conversation history was saved
    session_data = tutor_service.session_repo.get_session(user_id)
    assert "conversation_history" in session_data
    assert len(session_data["conversation_history"]) == 2  # user + assistant


def test_answer_question_with_history(tutor_service, mock_ai_engine):
    """Test that conversation history is used for context."""
    user_id = "test_user_history"
    
    # First question
    tutor_service.answer_question("What is Python?", user_id=user_id)
    
    # Second question with history
    tutor_service.answer_question("Tell me more", user_id=user_id, use_history=True)
    
    # Verify AI engine was called with conversation history
    call_args = mock_ai_engine.generate_answer.call_args_list[1]
    conversation_history = call_args[0][1]
    assert conversation_history is not None
    assert len(conversation_history) > 0


def test_answer_question_without_history(tutor_service, mock_ai_engine):
    """Test question answering without using history."""
    user_id = "test_user_no_history"
    
    # Add some history
    tutor_service.answer_question("What is Python?", user_id=user_id)
    
    # Ask new question without history
    tutor_service.answer_question("What is Java?", user_id=user_id, use_history=False)
    
    # Verify AI engine was called without conversation history
    call_args = mock_ai_engine.generate_answer.call_args_list[1]
    conversation_history = call_args[0][1]
    assert conversation_history is None


def test_provide_code_feedback_basic(tutor_service, mock_ai_engine):
    """Test basic code feedback without session."""
    code = "def add(a, b):\n    return a + b"
    language = "Python"
    
    feedback = tutor_service.provide_code_feedback(code, language)
    
    assert isinstance(feedback, str)
    assert len(feedback) > 0
    assert feedback == "This is mocked feedback"
    mock_ai_engine.analyze_code.assert_called_once()


def test_provide_code_feedback_with_context(tutor_service, mock_ai_engine):
    """Test code feedback with context."""
    code = "def multiply(x, y): return x * y"
    language = "Python"
    context = "Simple multiplication function"
    
    feedback = tutor_service.provide_code_feedback(code, language, context=context)
    
    assert isinstance(feedback, str)
    # Verify context was passed to AI engine
    mock_ai_engine.analyze_code.assert_called_with(code, language, context)


def test_provide_code_feedback_with_user_id(tutor_service, mock_ai_engine):
    """Test code feedback with user session tracking."""
    code = "print('hello')"
    language = "Python"
    user_id = "test_coder"
    
    feedback = tutor_service.provide_code_feedback(code, language, user_id=user_id)
    
    # Verify submission was saved to session
    session_data = tutor_service.session_repo.get_session(user_id)
    assert "code_submissions" in session_data
    assert len(session_data["code_submissions"]) == 1
    assert session_data["code_submissions"][0]["code"] == code
    assert session_data["code_submissions"][0]["language"] == language


def test_clear_session(tutor_service):
    """Test clearing user session."""
    user_id = "test_clear"
    
    # Create session with data
    tutor_service.answer_question("test", user_id=user_id)
    session_data = tutor_service.session_repo.get_session(user_id)
    assert "conversation_history" in session_data
    
    # Clear session
    tutor_service.clear_session(user_id)
    
    # Verify session is cleared (may still have metadata)
    session_data = tutor_service.session_repo.get_session(user_id)
    # After clearing, session should not have conversation_history
    assert "conversation_history" not in session_data


def test_get_session_summary_empty(tutor_service):
    """Test session summary for new user."""
    user_id = "new_user"
    summary = tutor_service.get_session_summary(user_id)
    
    assert summary["total_questions"] == 0
    assert summary["total_code_submissions"] == 0
    assert summary["has_active_session"] is False


def test_get_session_summary_with_data(tutor_service, mock_ai_engine):
    """Test session summary with activity."""
    user_id = "active_user"
    
    # Add some activity
    tutor_service.answer_question("What is Python?", user_id=user_id)
    tutor_service.answer_question("What is Java?", user_id=user_id)
    tutor_service.provide_code_feedback("code", "Python", user_id=user_id)
    
    summary = tutor_service.get_session_summary(user_id)
    
    assert summary["total_questions"] == 2
    assert summary["total_code_submissions"] == 1
    assert summary["has_active_session"] is True


def test_conversation_history_limit(tutor_service, mock_ai_engine):
    """Test that conversation history is limited to last 10 messages."""
    user_id = "chatty_user"
    
    # Add more than 10 messages (5 exchanges = 10 messages)
    for i in range(7):
        tutor_service.answer_question(f"Question {i}", user_id=user_id)
    
    session_data = tutor_service.session_repo.get_session(user_id)
    conversation_history = session_data["conversation_history"]
    
    # Should keep only last 10 messages
    assert len(conversation_history) == 10
