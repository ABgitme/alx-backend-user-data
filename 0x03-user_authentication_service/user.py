#!/usr/bin/env python3
"""Defines the User SQLAlchemy model for the 'users' table."""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for the 'users' table.

    Attributes:
        id (int): The primary key of the users table,
        auto-incremented.
        email (str): The user's email, non-nullable,
        and unique, max length 250.
        hashed_password (str): The user's hashed password,
        non-nullable, max length 250.
        session_id (str): The user's session ID,
        nullable, max length 250.
        reset_token (str): The user's password reset token,
        nullable, max length 250.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
