from fastapi import Depends
from sqlmodel import Session
from ..database.session import get_session
from ..models.user import User
from ..auth.utils import get_current_user


# Dependency to get the current authenticated user
CurrentUser = Depends(get_current_user)

# Dependency to get database session
SessionDep = Depends(get_session)

# Convenience function to get both session and current user
async def get_current_user_with_session(
    session: Session = SessionDep,
    current_user: User = CurrentUser
):
    return session, current_user