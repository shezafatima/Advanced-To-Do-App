#!/usr/bin/env python3
"""
Test script to simulate the exact API registration flow
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_api_flow():
    # Import the exact same modules as the API
    from sqlmodel import Session
    from src.database.session import engine
    from src.models.user import UserCreate
    from src.services.user_service import UserService
    from src.api.auth import register_user
    from fastapi import HTTPException

    print("Testing the exact API registration flow...")

    # Create a user creation object like the API would
    user_create = UserCreate(
        email="testuser@example.com",
        password="testpass123"
    )

    # Simulate the session dependency like FastAPI would
    try:
        with Session(engine) as session:
            print("Calling register_user function...")
            result = register_user(user_create=user_create, session=session)
            print(f"Registration successful: {result}")
    except HTTPException as e:
        print(f"HTTP Exception: {e.detail}, status: {e.status_code}")
    except Exception as e:
        print(f"General Exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_flow()