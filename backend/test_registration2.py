#!/usr/bin/env python3
"""
Test script to directly test the user registration functionality - fresh import
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_registration_fresh():
    from sqlmodel import Session
    from src.database.session import engine
    from src.models.user import UserCreate
    from src.services.user_service import UserService
    from src.config import settings

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

            # Test login as well
            from src.auth.jwt import verify_password, get_password_hash
            print("Testing password hashing...")
            hashed = get_password_hash("testpass123")
            verified = verify_password("testpass123", hashed)
            print(f"Password verification: {verified}")

    except Exception as e:
        print(f"Error during user creation: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_registration_fresh()