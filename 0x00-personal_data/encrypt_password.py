#!/usr/bin/env python3
"""
This module provides functions for password hashing
and validation using bcrypt.

Functions:
    hash_password(password: str) -> bytes
        Hashes a plain text password with a randomly generated salt and returns
        the hashed password as a byte string.

    is_valid(hashed_password: bytes, password: str) -> bool
        Validates a plain text password against a previously hashed password,
        returning True if they match and False otherwise.

This module is intended for securely handling
password storage and verification.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password with a salt using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password using bcrypt and return the hashed password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain text password to validate.

    Returns:
        bool: True if the password matches the hashed password,
            False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
