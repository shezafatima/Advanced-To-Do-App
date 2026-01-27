from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the most minimal FastAPI app possible
app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Minimal Todo API for Railway deployment"
)

# Minimal CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Only the essential endpoints that must respond immediately
@app.get("/")
def read_root():
    return {"message": "Todo API is running", "status": "success"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}

@app.get("/ready")
def ready_check():
    return {"ready": True}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)