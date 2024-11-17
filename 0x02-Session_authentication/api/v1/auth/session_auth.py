#!/usr/bin/env python3
""" Module of Session Authentication
"""
from api.v1.auth.auth import Auth
import uuid
from typing import Optional
from models.user import User
import os


class SessionAuth(Auth):
    """Session-based Authentication mechanism"""
    # Class attribute for storing user sessions
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user_id and stores it.

        Args:
            user_id (str): The ID of the user for whom to create a session.

        Returns:
            str: The generated Session ID, or None if user_id is invalid.
        """
        # Validate user_id
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique Session ID
        session_id = str(uuid.uuid4())

        # Store the session in the dictionary with user_id as the value
        self.user_id_by_session_id[session_id] = user_id

        # Return the created Session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the User ID associated with a given Session ID.

        Args:
            session_id (str): The Session ID to look up.

        Returns:
            str: The User ID associated with the session_id,
            or None if not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        # Retrieve user_id based on session_id
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> Optional[User]:
        """Retrieve the User instance based on the session ID from the cookie.

        Args:
            request: The Flask request object containing cookies.

        Returns:
            Optional[User]: The User instance if found, otherwise None.
        """
        # Retrieve the session ID from the request cookies
        session_id = self.session_cookie(request)

        # If session ID is None, return None
        if session_id is None:
            return None

        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)

        # Return None if no user ID is found
        if user_id is None:
            return None

        # Retrieve and return the User instance based on the user ID
        return User.get(user_id)
