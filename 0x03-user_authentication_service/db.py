#!/usr/bin/env python3
"""
DB module implement the add_user method
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class for interacting with the database."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        # Create a new User object
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            # Add the user to the session and commit the transaction
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            new_user = None
        # Return the newly created User object
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter users.

        Returns:
            User: The first User object that matches the filters.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If the query arguments are invalid.
        """
        if not kwargs:
            raise InvalidRequestError()

        user = self._session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        raise NoResultFound()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing
            the attributes to update.

        Returns:
            None

        Raises:
            ValueError: If any of the provided keys do not
            correspond to a valid user attribute.
        """
        # Find the user by ID
        user = self.find_user_by(id=user_id)

        # Validate the attributes to update
        valid_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in valid_columns:
                raise ValueError()

        # Update the user attributes
        for key, value in kwargs.items():
            setattr(user, key, value)

        # Commit changes to the database
        self._session.commit()
