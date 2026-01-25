from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth import router as auth_router
from src.api.todos import router as todos_router
from src.api.profiles import router as profiles_router
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

# Skip startup/shutdown events for serverless deployment
# The scheduler functionality is not suitable for serverless environments
# where instances are ephemeral

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}