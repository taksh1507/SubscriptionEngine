"""
subscriptions.py
----------------
Defines all API endpoints for managing subscription plans and user subscriptions.
Each endpoint is documented with its purpose and expected behavior.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.crud import subscription as crud
from app.schemas.subscription import (
    Plan, PlanCreate,
    Subscription, SubscriptionCreate, SubscriptionUpdate
)
from app.schemas.response import PaginatedResponse
from app.api import deps
from app.models.user import User
import logging

# Create a router for subscription-related endpoints
router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/plans/", response_model=Plan)
def create_plan(
    plan: PlanCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """Create a new subscription plan (Admin only)."""
    return crud.create_plan(db=db, plan=plan)

@router.get("/plans/", response_model=PaginatedResponse[Plan])
def get_plans(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Retrieve all available subscription plans."""
    plans, total = crud.get_plans(db=db, skip=skip, limit=limit)
    return PaginatedResponse(items=plans, total=total, skip=skip, limit=limit)

@router.post("/subscriptions/", response_model=Subscription)
def create_subscription(
    subscription: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Create a new subscription for a user."""
    if current_user.id != subscription.user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    logger.info(f"Creating subscription for user: {subscription.user_id}")
    try:
        subscription_result = crud.create_subscription(db=db, subscription=subscription)
        logger.info(f"Subscription created successfully for user: {subscription.user_id}")
        return subscription_result
    except ValueError as e:
        logger.error(f"Error creating subscription for user {subscription.user_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/subscriptions/{user_id}", response_model=Subscription)
def get_user_subscription(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Retrieve a user's active subscription by user ID."""
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    logger.info(f"Retrieving subscription for user_id: {user_id}")
    subscription = crud.get_user_subscription(db=db, user_id=user_id)
    if not subscription:
        logger.warning(f"Subscription not found for user_id: {user_id}")
        raise HTTPException(status_code=404, detail="Subscription not found")
    logger.info(f"Subscription retrieved successfully for user_id: {user_id}")
    return subscription

@router.put("/subscriptions/{user_id}", response_model=Subscription)
def update_subscription(
    user_id: int,
    subscription_update: SubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Update a user's subscription (e.g., change plan or status)."""
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    try:
        return crud.update_subscription(
            db=db,
            user_id=user_id,
            subscription_update=subscription_update
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/subscriptions/{user_id}", response_model=Subscription)
def cancel_subscription(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """Cancel a user's active subscription."""
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    try:
        return crud.cancel_subscription(db=db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 