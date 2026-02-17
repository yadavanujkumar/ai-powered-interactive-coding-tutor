class SessionRepository:
    def __init__(self):
        self.sessions = {}

    def save_session(self, user_id: str, data: dict):
        """Save user session data."""
        self.sessions[user_id] = data

    def get_session(self, user_id: str) -> dict:
        """Retrieve user session data."""
        return self.sessions.get(user_id, {})
