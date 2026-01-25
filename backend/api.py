# Vercel-compatible ASGI entry point
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import the serverless-compatible app
from vercel_app import app

# This is the ASGI application that Vercel will use
application = app