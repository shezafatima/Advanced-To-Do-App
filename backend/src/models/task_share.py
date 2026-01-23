from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Dict, Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg

if TYPE_CHECKING:
    from .user import User
    from .todo import Todo


class RoleEnum(str, Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"


class TaskShareBase(SQLModel):
    task_id: UUID = Field(foreign_key="todo.id", nullable=False)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    role: RoleEnum = Field(default=RoleEnum.viewer)
    permissions: str = Field(default='{}', max_length=1000)  # JSON as string


class TaskShare(TaskShareBase, table=True):
    """
    Task Share model for managing task collaboration relationships.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    shared_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships - commented out temporarily to avoid circular import issues
    # task: "Todo" = Relationship(back_populates="shares", link_model=None)
    # user: "User" = Relationship(back_populates="task_shares", link_model=None)


class TaskShareRead(TaskShareBase):
    """
    Schema for reading task share data.
    """
    id: UUID
    shared_at: datetime


class TaskShareCreate(TaskShareBase):
    """
    Schema for creating a new task share.
    """
    task_id: UUID
    user_id: UUID
    role: RoleEnum


class TaskShareUpdate(SQLModel):
    """
    Schema for updating a task share.
    """
    role: Optional[RoleEnum] = None
    permissions: Optional[str] = None