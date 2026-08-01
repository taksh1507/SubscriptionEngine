"""
main.py
--------
Entry point for the Subscription Microservice.
Sets up the FastAPI app, middleware, and includes all API routes.
Run this file to start the server.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
import logging
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.scheduler import start_scheduler, shutdown_scheduler

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting background tasks...")
    start_scheduler()
    yield
    logger.info("Shutting down background tasks...")
    shutdown_scheduler()

# Create the FastAPI application instance
app = FastAPI(
    title="Subscription Service",
    description="A microservice for managing user subscriptions",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for all origins (for development; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal database error occurred."},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# Register the API router under the /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    # Run the app with Uvicorn for local development
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 