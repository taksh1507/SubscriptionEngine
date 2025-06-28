"""
main.py
--------
Entry point for the Subscription Microservice.
Sets up the FastAPI app, middleware, and includes all API routes.
Run this file to start the server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

# Create the FastAPI application instance
app = FastAPI(
    title="Subscription Service",
    description="A microservice for managing user subscriptions",
    version="1.0.0"
)

# Enable CORS for all origins (for development; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the API router under the /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    # Run the app with Uvicorn for local development
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 