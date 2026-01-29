from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from sqlalchemy import create_engine, inspect
from src.database.session import get_engine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Track initialization status
db_initialized = False

def initialize_database():
    """Initialize database tables on startup"""
    global db_initialized
    if not db_initialized:
        try:
            logger.info("Initializing database tables...")
            engine = get_engine()

            # Check if tables exist
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()

            if not existing_tables or 'user' not in existing_tables:
                # Create all tables if none exist or critical tables are missing
                SQLModel.metadata.create_all(bind=engine)
                logger.info("Database tables created successfully!")
            else:
                logger.info("Database tables already exist, skipping initialization")

            db_initialized = True
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up application...")
    initialize_database()
    logger.info("Application startup complete.")

    yield  # Run the application

    # Shutdown
    logger.info("Shutting down application...")

# Create the FastAPI app with lifespan
app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Todo API with full functionality for production deployment",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Essential endpoints that must respond immediately
@app.get("/")
def read_root():
    return {"message": "Todo API is running", "status": "success"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}

@app.get("/ready")
def ready_check():
    return {"ready": True}

# Import and add the full API functionality after basic setup
try:
    from src.api.auth import router as auth_router
    from src.api.todos import router as todos_router
    from src.api.profiles import router as profiles_router

    # Register the full API routes
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(todos_router, prefix="/todos", tags=["Todos"])
    app.include_router(profiles_router, prefix="/profiles", tags=["Profiles"])

    logger.info("Full API routes registered successfully")
except ImportError as e:
    logger.error(f"Could not import full API routes: {e}")
    # Add fallback endpoints if full API routes fail to load
    @app.get("/auth/status")
    def auth_status():
        return {"status": "auth service not available"}

    @app.get("/todos/status")
    def todos_status():
        return {"status": "todos service not available"}

    @app.get("/profiles/status")
    def profiles_status():
        return {"status": "profiles service not available"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)