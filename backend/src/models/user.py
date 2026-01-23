from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg

if TYPE_CHECKING:
    from .todo import Todo  # Only import for type checking
    from .profile import UserProfile
    from .task_share import TaskShare
    from .notification import Notification


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    """
    User model representing a registered user of the application.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships - using string references to avoid circular imports
    # todos: List["Todo"] = Relationship(sa_relationship="Todo", back_populates="user")
    # profile: "UserProfile" = Relationship(sa_relationship="UserProfile", back_populates="user")
    # task_shares: List["TaskShare"] = Relationship(sa_relationship="TaskShare", back_populates="user")
    # notifications: List["Notification"] = Relationship(sa_relationship="Notification", back_populates="user")


class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information).
    """
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    email: Optional[str] = None
    password: Optional[str] = None