from sqlmodel import SQLModel
from .session import engine
from ..models.user import User
from ..models.todo import Todo


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    """
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()