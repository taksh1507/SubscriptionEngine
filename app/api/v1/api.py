"""
api.py
------
Collects and organizes all API routes for version 1 of the API.
"""
import logging

from fastapi import APIRouter
from app.api.v1.endpoints import subscriptions, auth, users

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()
logger.info("Including routers")
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(subscriptions.router, tags=["subscriptions"])
logger.info("Routers included")