# api/v1/auth/session_db_auth.py

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from typing import Optional
from flask import request


class SessionDBAuth(SessionExpAuth):
    """Session-based authentication with database persistence."""

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """Create a new session and store it in UserSession."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store the session in UserSession model
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(
            self, session_id: Optional[str] = None) -> Optional[str]:
        """Retrieve the user ID associated with the given session_id."""
        if session_id is None:
            return None

        # Retrieve session from UserSession model
        session = UserSession.search({"session_id": session_id})
        if not session:
            return None

        return session[0].user_id if session else None

    def destroy_session(self, request=None) -> bool:
        """Destroy a session by removing it from UserSession."""
        if request is None:
            return False

        # Retrieve session ID from the cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Retrieve and delete the UserSession
        session = UserSession.search({"session_id": session_id})
        if not session:
            return False

        session[0].remove()  # Remove the session from the file database
        return True
