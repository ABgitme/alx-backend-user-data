#!/usr/bin/env python3
"""
_hash_password method using bcrypt.hashpw
to hash a password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Generate a salted hash of the input password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")

    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password using bcrypt and the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password
