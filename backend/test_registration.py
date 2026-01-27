#!/usr/bin/env python3
"""
Test script to directly test the user registration functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from sqlmodel import Session
from src.database.session import engine
from src.models.user import UserCreate
from src.services.user_service import UserService
from src.config import settings

def test_registration():
    print("Starting user registration test...")

    try:
        # Create a session
        with Session(engine) as session:
            # Create test user data with a shorter password
            user_data = UserCreate(
                email="test@example.com",
                password="testpass123"  # Shorter password to avoid bcrypt 72 char limit
            )

            print("Attempting to create user...")
            user = UserService.create_user(session=session, user_create=user_data)
            print(f"User created successfully: {user.email}, ID: {user.id}")

    except Exception as e:
        print(f"Error during user creation: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_registration()