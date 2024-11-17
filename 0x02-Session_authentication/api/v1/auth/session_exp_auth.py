#!/usr/bin/env python3
"""session expiration functionality"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration time."""

    def __init__(self):
        """Initialize SessionExpAuth with session duration."""
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", "0"))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID with an expiration date
        for the given user_id."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store the session data with user_id and created_at time
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve the user ID from the session ID, considering expiration."""
        if session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if not session_data:
            return None

        user_id = session_data.get("user_id")
        created_at = session_data.get("created_at")
        if not created_at:
            return None

        # If session_duration is 0 or less,
        # return user_id without expiration check
        if self.session_duration <= 0:
            return user_id

        # Check if session is expired
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return user_id
