#!/usr/bin/env python3
"""
BasicAuth module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the Authorization
            header if valid, else None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        # Return the part after "Basic " (space included)
        return authorization_header[len("Basic "):]
