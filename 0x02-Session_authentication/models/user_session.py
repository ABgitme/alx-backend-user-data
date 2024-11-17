# models/user_session.py

from models.base import Base


class UserSession(Base):
    """UserSession model for storing sessions in the database."""
    
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance with user_id
        and session_id."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
