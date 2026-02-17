from src.repositories.session_repository import SessionRepository

def test_save_and_get_session():
    repo = SessionRepository()
    user_id = "user123"
    data = {"question": "What is Python?"}

    repo.save_session(user_id, data)
    retrieved_data = repo.get_session(user_id)

    assert retrieved_data == data

def test_get_session_no_data():
    repo = SessionRepository()
    user_id = "nonexistent_user"

    retrieved_data = repo.get_session(user_id)

    assert retrieved_data == {}
