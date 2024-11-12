#!/usr/bin/env python3
"""
Authentication module for the API
"""
from typing import List, TypeVar
from flask import request


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request
        """
        return None
