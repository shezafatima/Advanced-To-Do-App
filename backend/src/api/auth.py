from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Any
from pydantic import BaseModel
from ..database.session import get_session
from ..models.user import User, UserCreate, UserRead
from ..auth.jwt import verify_password, create_access_token
from ..services.user_service import UserService
from ..utils.errors import ErrorResponse
from ..api.deps import CurrentUser
from ..auth.utils import get_current_user


class LoginRequest(BaseModel):
    email: str
    password: str


router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    try:
        user = UserService.create_user(session=session, user_create=user_create)
        return user
    except HTTPException:
        # Re-raise HTTP exceptions (like DuplicateEmailException)
        raise
    except Exception as e:
        # Log the error for debugging
        import traceback
        print(f"Registration error: {str(e)}")
        print(traceback.format_exc())

        # Raise a generic server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration. Please try again."
        )


@router.post("/login")
async def login_user(login_request: LoginRequest, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token.
    """
    email = login_request.email
    password = login_request.password

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    user = UserService.get_user_by_email(session=session, email=email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Get current user info.
    """
    return current_user