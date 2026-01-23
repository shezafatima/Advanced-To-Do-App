from sqlmodel import SQLModel

# Import all models to ensure they're registered with SQLModel's metadata
from .todo import Todo
from .user import User
from .tag import Tag
from .profile import UserProfile
from .task_share import TaskShare
from .notification import Notification


# Base model for all SQLModel classes
class Base(SQLModel):
    pass


__all__ = ["SQLModel", "Base", "Todo", "User", "Tag", "UserProfile", "TaskShare", "Notification"]