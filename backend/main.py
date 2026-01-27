# Entry point for Hugging Face Spaces
# This file is created to satisfy containers that look for a main module
import os
# Set default database URL before any imports
if not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///./todo_app_hf.db'

from app import app

# This makes the FastAPI app available as 'main:app' if needed
# The original app is available as 'app:app' as configured in Dockerfile
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)