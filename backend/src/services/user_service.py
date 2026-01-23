from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate, UserUpdate
from ..auth.jwt import get_password_hash
from ..utils.errors import DuplicateEmailException, UserNotFoundException


class UserService:
    """
    Service class for handling user-related operations.
    """

    @staticmethod
    def create_user(*, session: Session, user_create: UserCreate) -> User:
        """
        Create a new user with the given data.
        """
        # Check if user with this email already exists
        existing_user = session.exec(
            select(User).where(User.email == user_create.email)
        ).first()

        if existing_user:
            raise DuplicateEmailException()

        # Create the user
        user = User(
            email=user_create.email,
            hashed_password=get_password_hash(user_create.password)
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def get_user_by_id(*, session: Session, user_id: str) -> Optional[User]:
        """
        Get a user by their ID.
        """
        user = session.get(User, user_id)
        return user

    @staticmethod
    def get_user_by_email(*, session: Session, email: str) -> Optional[User]:
        """
        Get a user by their email.
        """
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        return user

    @staticmethod
    def update_user(*, session: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """
        Update a user with the given data.
        """
        user = session.get(User, user_id)

        if not user:
            raise UserNotFoundException(user_id)

        # Update fields if provided
        if user_update.email is not None:
            # Check if new email is already taken
            existing_user = session.exec(
                select(User).where(User.email == user_update.email)
            ).first()

            if existing_user and existing_user.id != user.id:
                raise DuplicateEmailException()

            user.email = user_update.email

        if user_update.password is not None:
            user.hashed_password = get_password_hash(user_update.password)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def delete_user(*, session: Session, user_id: str) -> bool:
        """
        Delete a user by their ID.
        """
        user = session.get(User, user_id)

        if not user:
            return False

        session.delete(user)
        session.commit()

        return True