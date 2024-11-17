#!/usr/bin/env python3
"""
auth.py - Authentication module for the API

This module contains the Auth class,
which provides methods for handling
authentication, including determining
if a given path requires authentication,
retrieving the authorization header,
and getting the current user.

The Auth class is intended to be a base
class for more specific authentication
mechanisms.
"""
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """
    A base class for API authentication.

    This class provides foundational methods
    for authentication handling in the API.
    It includes methods to:
    - Determine if a specific path requires authentication
    - Retrieve the authorization header from a request
    - Identify the current user based on a request
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication
        """
        if path is None or excluded_paths is None:
            return True

        # Normalize the path by removing any trailing slash
        normalized_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            # If excluded_path ends with '*', treat it as a prefix
            if excluded_path.endswith('*'):
                # Remove the trailing '*' and normalize the excluded path
                normalized_excluded_path = excluded_path.\
                        rstrip('*').rstrip('/')

                # If the normalized path starts with
                # the normalized excluded path, return False
                if normalized_path.startswith(normalized_excluded_path):
                    return False
            else:
                # Normalize the excluded path and compare it to the path
                normalized_excluded_path = excluded_path.rstrip('/')
                if normalized_path == normalized_excluded_path:
                    return False

        # If no match is found, the path requires authentication
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a Flask request object
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request.

        Args:
            request (flask.Request): The request object containing cookies.

        Returns:
            str or None: The value of the session cookie, or None if not found.
        """
        # Return None if the request is not provided
        if request is None:
            return None

        # Retrieve the session cookie name from environment variable
        session_name = os.getenv("SESSION_NAME", "_my_session_id")

        # Use .get() to retrieve the cookie value safely
        return request.cookies.get(session_name)
