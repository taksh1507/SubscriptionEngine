"""
api.py
------
Collects and organizes all API routes for version 1 of the API.
"""
import logging

from fastapi import APIRouter
from app.api.v1.endpoints import subscriptions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_router = APIRouter()
logger.info("Including subscriptions router")
api_router.include_router(subscriptions.router, tags=["subscriptions"])
logger.info("Subscriptions router included")