"""
subscription.py (Schemas)
-------------------------
Defines Pydantic models for request and response validation.
Ensures data integrity for API input and output.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import logging
from app.models.subscription import SubscriptionStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlanBase(BaseModel):
    name: str
    price: float
    features: str
    duration_days: int

class PlanCreate(PlanBase):
    pass

class Plan(PlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    def __init__(self, *args, **kwargs):
        logger.info(f"Creating Plan instance with id: {kwargs.get('id')}, name: {kwargs.get('name')}")
        super().__init__(*args, **kwargs)
        logger.info(f"Plan instance created with id: {self.id}")

class SubscriptionBase(BaseModel):
    user_id: int
    plan_id: int

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    plan_id: Optional[int] = None
    status: Optional[SubscriptionStatus] = None

class Subscription(SubscriptionBase):
    id: int
    status: SubscriptionStatus
    start_date: datetime
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    plan: Plan

    class Config:
        from_attributes = True

    def __init__(self, *args, **kwargs):
        logger.info(f"Creating Subscription instance with id: {kwargs.get('id')}, user_id: {kwargs.get('user_id')}, plan_id: {kwargs.get('plan_id')}")
        super().__init__(*args, **kwargs)
        logger.info(f"Subscription instance created with id: {self.id}")