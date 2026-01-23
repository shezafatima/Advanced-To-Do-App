from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from .user import User


class UserProfileBase(SQLModel):
    display_name: str = Field(nullable=False, max_length=100)
    preferred_language: str = Field(default="en", max_length=10)  # en, ur, etc.
    theme_preference: Optional[str] = Field(default=None, max_length=20)  # dark, light, auto
    notification_preferences: str = Field(default='{"toast_notifications": true}', max_length=1000)  # JSON as string

    class Config:
        populate_by_name = True
        alias_generator = lambda field_name: ''.join(
            word.capitalize() if i > 0 else word
            for i, word in enumerate(field_name.split('_'))
        )


class UserProfile(UserProfileBase, table=True):
    """
    User Profile model containing personalization settings and preferences.
    """
    __tablename__ = "user_profile"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", unique=True, nullable=False)
    avatar: Optional[bytes] = Field(default=None, max_length=2097152)  # Max 2MB
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationship to user - commented out temporarily to avoid circular import issues
    # user: "User" = Relationship(back_populates="profile", link_model=None)


class UserProfileRead(UserProfileBase):
    """
    Schema for reading user profile data.
    """
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        alias_generator = lambda field_name: ''.join(
            word.capitalize() if i > 0 else word
            for i, word in enumerate(field_name.split('_'))
        )


class UserProfileCreate(UserProfileBase):
    """
    Schema for creating a new user profile.
    """
    display_name: str = Field(min_length=1, max_length=100)

    class Config:
        populate_by_name = True
        alias_generator = lambda field_name: ''.join(
            word.capitalize() if i > 0 else word
            for i, word in enumerate(field_name.split('_'))
        )


from pydantic import Field as PydanticField

class UserProfileUpdate(SQLModel):
    """
    Schema for updating user profile.
    """
    display_name: Optional[str] = PydanticField(default=None, alias="displayName")
    preferred_language: Optional[str] = PydanticField(default=None, alias="preferredLanguage")
    theme_preference: Optional[str] = PydanticField(default=None, alias="themePreference")
    notification_preferences: Optional[Dict[str, Any]] = PydanticField(default=None, alias="notificationPreferences")
    avatar: Optional[bytes] = PydanticField(default=None, alias="avatar")

    class Config:
        populate_by_name = True