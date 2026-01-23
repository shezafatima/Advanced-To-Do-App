from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Standard error response model.
    """
    detail: str


class TodoException(HTTPException):
    """
    Base exception for todo-related errors.
    """
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundException(TodoException):
    """
    Exception raised when a user is not found.
    """
    def __init__(self, user_id: str):
        super().__init__(
            detail=f"User with id {user_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class TodoNotFoundException(TodoException):
    """
    Exception raised when a todo is not found.
    """
    def __init__(self, todo_id: str):
        super().__init__(
            detail=f"Todo with id {todo_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class UnauthorizedAccessException(TodoException):
    """
    Exception raised when a user tries to access a resource they don't own.
    """
    def __init__(self):
        super().__init__(
            detail="You are not authorized to access this resource",
            status_code=status.HTTP_403_FORBIDDEN
        )


class DuplicateEmailException(TodoException):
    """
    Exception raised when trying to create a user with an existing email.
    """
    def __init__(self):
        super().__init__(
            detail="A user with this email already exists",
            status_code=status.HTTP_400_BAD_REQUEST
        )


class TagNotFoundException(TodoException):
    """
    Exception raised when a tag is not found.
    """
    def __init__(self, tag_id: str):
        super().__init__(
            detail=f"Tag with id {tag_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


def handle_error(detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    """
    Helper function to raise HTTP exceptions with standard format.
    """
    raise HTTPException(status_code=status_code, detail=detail)