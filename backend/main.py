# Entry point for Railway deployment
# This file is created to satisfy containers that look for a main module

# Import the minimal app to avoid any complex initialization
from app import app

# This makes the FastAPI app available as 'main:app' for Railway
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)