from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg

if TYPE_CHECKING:
    from .user import User
    from .tag import Tag


class TagRead(SQLModel):
    id: UUID
    name: str
    color: str
    created_at: datetime


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TodoBase(SQLModel):
    title: str = Field(nullable=False, max_length=500)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)


class Todo(TodoBase, table=True):
    """
    Advanced Todo model representing a personal task item with enhanced features.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    priority: PriorityEnum = Field(default=PriorityEnum.medium)
    due_date: Optional[datetime] = Field(default=None)
    recurrence_rule: Optional[str] = Field(default=None, max_length=255)  # RFC 5545 format
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationship to user - commented out temporarily to avoid circular import issues
    # user: "User" = Relationship(back_populates="todos", link_model=None)

    # Many-to-many relationship with tags (defined via string to avoid circular imports)
    # tags: List["Tag"] = Relationship(
    #     back_populates="todos",
    #     link_model="TodoTag"
    # )


class TodoRead(TodoBase):
    """
    Schema for reading todo data.
    """
    id: UUID
    user_id: UUID
    priority: PriorityEnum
    due_date: Optional[datetime]
    recurrence_rule: Optional[str]
    created_at: datetime
    updated_at: datetime


class TodoCreate(TodoBase):
    """
    Schema for creating a new todo.
    """
    title: str = Field(min_length=1, max_length=500)
    priority: Optional[PriorityEnum] = PriorityEnum.medium
    due_date: Optional[datetime] = None
    recurrence_rule: Optional[str] = None


class TodoUpdate(SQLModel):
    """
    Schema for updating a todo.
    """
    title: Optional[str] = Field(default=None, max_length=500)
    description: Optional[str] = Field(default=None)
    completed: Optional[bool] = Field(default=None)
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None
    recurrence_rule: Optional[str] = None


class TodoToggle(SQLModel):
    """
    Schema for toggling todo completion status.
    """
    completed: bool


class TodoAdvancedRead(TodoRead):
    """
    Extended schema for reading todo data with all advanced features.
    """
    tags: List['TagRead'] = []