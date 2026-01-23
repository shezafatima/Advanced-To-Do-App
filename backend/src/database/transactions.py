from contextlib import contextmanager
from sqlmodel import Session, select
from typing import Generator
from ..database.session import engine


@contextmanager
def get_db_transaction() -> Generator[Session, None, None]:
    """
    Context manager for database transactions.
    Ensures that the transaction is committed if successful, or rolled back if an exception occurs.
    """
    with Session(engine) as session:
        try:
            # Begin transaction
            yield session
            # Commit transaction if no exceptions occurred
            session.commit()
        except Exception as e:
            # Rollback transaction in case of an exception
            session.rollback()
            raise e


def execute_in_transaction(func, *args, **kwargs):
    """
    Execute a function within a database transaction.

    Args:
        func: The function to execute within the transaction
        *args, **kwargs: Arguments to pass to the function

    Returns:
        The result of the function execution
    """
    with get_db_transaction() as session:
        return func(session, *args, **kwargs)


def batch_insert(session: Session, model_class, data_list: list):
    """
    Perform a batch insert operation.

    Args:
        session: Database session
        model_class: The SQLModel class to insert
        data_list: List of dictionaries containing data to insert
    """
    objects = [model_class(**data) for data in data_list]
    session.add_all(objects)
    return objects