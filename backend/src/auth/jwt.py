from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from ..config import settings
from ..models.user import User


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Note: bcrypt has a 72 character limit, so we truncate if necessary.
    """
    # Bcrypt has a 72 character limit
    truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
    return pwd_context.verify(truncated_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password.
    Note: bcrypt has a 72 character limit, so we truncate if necessary.
    """
    # Bcrypt has a 72 character limit
    truncated_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(truncated_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the given data and expiration time.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def verify_access_token(token: str) -> Optional[dict]:
    """
    Verify a JWT access token and return the payload if valid.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


def authenticate_user(email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    This function would typically be called from a service layer.
    """
    # This is a placeholder - actual implementation would query the database
    # to get the user and verify the password
    raise NotImplementedError("This function should be implemented in the user service")