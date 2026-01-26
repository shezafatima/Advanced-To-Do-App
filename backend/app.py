import os
# Set environment variables before any imports
if not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///./todo_app_hf.db'

# Set a short timeout for any potential database operations
os.environ.setdefault('STATE_CONNECT_TIMEOUT', '5')

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app with minimal setup
app = FastAPI(
    title="Todo API ",
    version="1.0.0",
    description="Todo API optimized ",
    # Reduce startup overhead
    lifespan=None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple static endpoints without database dependencies
@app.get("/")
def read_root():
    return {
        "message": "Todo API is running",
        "status": "success",
        "ready": True
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": "1.0.0"
    }

@app.get("/ready")
def ready_check():
    return {"ready": True}

# Placeholder endpoints - these won't work until we figure out the startup issue
@app.get("/todos")
def todos_placeholder():
    return {"message": "Todos API endpoint", "status": "placeholder"}

@app.get("/auth")
def auth_placeholder():
    return {"message": "Auth API endpoint", "status": "placeholder"}

@app.get("/profiles")
def profiles_placeholder():
    return {"message": "Profiles API endpoint", "status": "placeholder"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)