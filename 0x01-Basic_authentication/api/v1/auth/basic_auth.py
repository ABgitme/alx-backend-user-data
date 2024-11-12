#!/usr/bin/env python3
"""
BasicAuth module
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string.

        Args:
            base64_authorization_header (str):
            The Base64 string to decode.

        Returns:
            str: The decoded string as UTF-8,
            or None if decoding fails.
        """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode from Base64
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert bytes to UTF-8 string
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from
        the decoded Base64 authorization header.

        Args:
            decoded_base64_authorization_header (str):
            The decoded Base64 string.

        Returns:
            tuple: A tuple containing user email and
            password as strings, or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a User instance based on email and password.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance if authentication is successful;
            None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for users by email using the User class method
        users = User.search({"email": user_email})

        if not users:
            return None
        # Assuming unique email constraint, taking the first match
        user = users[0]
        if user is None or not user.is_valid_password(user_pwd):
            return None

        return user
