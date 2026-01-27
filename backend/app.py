import os
# Set environment variables before any imports
if not os.environ.get('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///./todo_app_hf.db'

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app without lifespan (to avoid startup delays)
app = FastAPI(
    title="Todo API for Production",
    version="1.0.0",
    description="Todo API with full functionality for production deployment"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routers (with error handling for deployment)
try:
    from src.api.auth import router as auth_router
    from src.api.todos import router as todos_router
    from src.api.profiles import router as profiles_router

    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(todos_router, prefix="/todos", tags=["Todos"])
    app.include_router(profiles_router, prefix="/profiles", tags=["Profiles"])

    logger.info("API routers imported and registered successfully")
except ImportError as e:
    logger.error(f"Error importing API routers: {e}")
    # Fallback: create basic placeholder endpoints
    @app.get("/auth/placeholder")
    def auth_placeholder():
        return {"error": "Auth module not available"}

    @app.get("/todos/placeholder")
    def todos_placeholder():
        return {"error": "Todos module not available"}

    @app.get("/profiles/placeholder")
    def profiles_placeholder():
        return {"error": "Profiles module not available"}

@app.get("/")
def read_root():
    return {
        "message": "Todo API is running",
        "status": "success",
        "ready": True
        # Removed database_url to prevent exposing credentials
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

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)