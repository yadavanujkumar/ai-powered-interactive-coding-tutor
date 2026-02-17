"""Tests for session repository."""
import pytest
from src.repositories.session_repository import SessionRepository


@pytest.fixture
def repo():
    """Create a session repository for testing."""
    return SessionRepository()


def test_save_and_get_session(repo):
    """Test saving and retrieving session data."""
    user_id = "user123"
    data = {"question": "What is Python?"}

    repo.save_session(user_id, data)
    retrieved_data = repo.get_session(user_id)

    assert "question" in retrieved_data
    assert retrieved_data["question"] == "What is Python?"
    assert "last_updated" in retrieved_data


def test_get_session_no_data(repo):
    """Test retrieving session for non-existent user."""
    user_id = "nonexistent_user"
    retrieved_data = repo.get_session(user_id)
    assert retrieved_data == {}


def test_delete_session(repo):
    """Test deleting a session."""
    user_id = "user456"
    data = {"test": "data"}
    
    repo.save_session(user_id, data)
    assert repo.session_exists(user_id)
    
    deleted = repo.delete_session(user_id)
    assert deleted is True
    assert not repo.session_exists(user_id)


def test_delete_nonexistent_session(repo):
    """Test deleting a session that doesn't exist."""
    deleted = repo.delete_session("nonexistent")
    assert deleted is False


def test_session_exists(repo):
    """Test checking if session exists."""
    user_id = "user789"
    assert not repo.session_exists(user_id)
    
    repo.save_session(user_id, {"data": "test"})
    assert repo.session_exists(user_id)


def test_save_session_empty_user_id(repo):
    """Test that saving with empty user_id raises error."""
    with pytest.raises(ValueError):
        repo.save_session("", {"data": "test"})


def test_get_session_empty_user_id(repo):
    """Test that getting with empty user_id raises error."""
    with pytest.raises(ValueError):
        repo.get_session("")


def test_update_session(repo):
    """Test updating existing session data."""
    user_id = "user_update"
    initial_data = {"count": 1}
    
    repo.save_session(user_id, initial_data)
    first_timestamp = repo.get_session(user_id)["last_updated"]
    
    # Update session
    updated_data = {"count": 2}
    repo.save_session(user_id, updated_data)
    
    retrieved = repo.get_session(user_id)
    assert retrieved["count"] == 2
    assert retrieved["last_updated"] >= first_timestamp
