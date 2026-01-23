from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router as auth_router
from .api.todos import router as todos_router
from .api.profiles import router as profiles_router
from .utils.scheduler import scheduler
import asyncio
import threading
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware - in production, configure properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be configured properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(todos_router, prefix="/todos", tags=["Todos"])
app.include_router(profiles_router, prefix="/profiles", tags=["Profiles"])

@app.on_event("startup")
async def startup_event():
    """Start the recurring task scheduler when the application starts."""
    logger.info("Starting up application...")
    # Start the scheduler in the background
    asyncio.create_task(scheduler.start())

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the recurring task scheduler when the application shuts down."""
    logger.info("Shutting down application...")
    await scheduler.stop()

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}