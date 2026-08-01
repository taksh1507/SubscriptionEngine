"""
subscription.py (Models)
-----------------------
Defines the SQLAlchemy models for subscription plans and user subscriptions.
Each model and field is documented for clarity.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import logging

from app.db.base_class import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SubscriptionStatus(str, enum.Enum):
    """
    Enum for possible subscription statuses.
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class Plan(Base):
    """
    Represents a subscription plan (e.g., Free, Pro, Enterprise).
    """
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    price = Column(Float, nullable=False)
    features = Column(String(500))
    duration_days = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        logger.info(f"Creating Plan instance with name: {kwargs.get('name')}")
        super().__init__(*args, **kwargs)
        logger.info(f"Plan instance created with id: {self.id}")

class Subscription(Base):
    """
    Represents a user's subscription to a plan.
    """
    __tablename__ = "subscriptions"
    __table_args__ = (
        Index('ix_subscription_user_status', 'user_id', 'status'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"))
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    plan = relationship("Plan")

    def __init__(self, *args, **kwargs):
        logger.info(f"Creating Subscription instance for user: {kwargs.get('user_id')}, plan: {kwargs.get('plan_id')}")
        super().__init__(*args, **kwargs)
        logger.info(f"Subscription instance created with id: {self.id}")