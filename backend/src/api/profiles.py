from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID
from ..database.session import get_session
from ..models.user import User
from ..models.profile import (
    UserProfile, UserProfileRead, UserProfileCreate, UserProfileUpdate
)
from ..services.todo_service import UserProfileService
from ..auth.utils import get_current_user
from datetime import datetime, timezone


router = APIRouter()


@router.get("/me", response_model=UserProfileRead)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get current user's profile.
    """
    profile = UserProfileService.get_profile_by_user_id(
        session=session,
        user_id=current_user.id
    )

    if not profile:
        # If no profile exists, create a default one
        profile = UserProfileService.create_profile(
            session=session,
            user_id=current_user.id,
            display_name=current_user.email.split('@')[0]  # Use email prefix as default display name
        )

    return profile


@router.put("/me", response_model=UserProfileRead)
async def update_my_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update current user's profile.
    """
    # Check if profile exists
    existing_profile = UserProfileService.get_profile_by_user_id(
        session=session,
        user_id=current_user.id
    )

    if not existing_profile:
        # If no profile exists, create one
        profile = UserProfileService.create_profile(
            session=session,
            user_id=current_user.id,
            display_name=profile_update.display_name or current_user.email.split('@')[0],
            preferred_language=profile_update.preferred_language or "en",
            theme_preference=profile_update.theme_preference,
            notification_preferences=profile_update.notification_preferences
        )
    else:
        # Update existing profile
        profile = UserProfileService.update_profile(
            session=session,
            user_id=current_user.id,
            profile_update=profile_update
        )

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile