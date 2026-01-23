from datetime import datetime, timezone
from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .todo import Todo


class TagBase(SQLModel):
    name: str = Field(nullable=False, max_length=50, unique=True)
    color: str = Field(nullable=False, max_length=7)  # hex color code like #ff6b6b


class Tag(TagBase, table=True):
    """
    Tag model for categorizing and organizing tasks.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    # Many-to-many relationship with todos (defined via string to avoid circular imports)
    # todos: List["Todo"] = Relationship(
    #     back_populates="tags",
    #     link_model="TodoTag"
    # )


class TagRead(TagBase):
    """
    Schema for reading tag data.
    """
    id: UUID
    created_at: datetime


class TagCreate(TagBase):
    """
    Schema for creating a new tag.
    """
    name: str = Field(min_length=1, max_length=50)


class TagUpdate(SQLModel):
    """
    Schema for updating a tag.
    """
    name: str = Field(default=None, max_length=50)
    color: str = Field(default=None, max_length=7)  # hex color code