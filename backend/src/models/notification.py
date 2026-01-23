from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .user import User


class NotificationTypeEnum(str, Enum):
    success = "success"
    error = "error"
    warning = "warning"
    info = "info"


class NotificationBase(SQLModel):
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    type: NotificationTypeEnum = Field(nullable=False)
    title: str = Field(nullable=False, max_length=100)
    message: str = Field(nullable=False, max_length=500)
    read: bool = Field(default=False)


class Notification(NotificationBase, table=True):
    """
    Notification model for tracking user alerts and notifications.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationship to user - commented out temporarily to avoid circular import issues
    # user: "User" = Relationship(back_populates="notifications", link_model=None)


class NotificationRead(NotificationBase):
    """
    Schema for reading notification data.
    """
    id: UUID
    created_at: datetime


class NotificationCreate(NotificationBase):
    """
    Schema for creating a new notification.
    """
    user_id: UUID
    type: NotificationTypeEnum
    title: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=500)


class NotificationUpdate(SQLModel):
    """
    Schema for updating notification status.
    """
    read: Optional[bool] = None