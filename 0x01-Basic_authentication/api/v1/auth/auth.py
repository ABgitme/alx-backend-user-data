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

        # Handle cases where excluded_paths is empty or None
        if not excluded_paths:
            return True

        # Remove trailing slash from the path if present (to ensure slash-tolerant matching)
        path = path.rstrip('/')

        for excluded_path in excluded_paths:
            # Handle wildcard in the excluded path (e.g., '/api/v1/stat*')
            if excluded_path.endswith('*'):
                # Remove the '*' and compare if the path starts with the prefix before '*'
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

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
