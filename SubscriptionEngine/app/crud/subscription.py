"""
subscription.py (CRUD)
---------------------
Contains all database operations (CRUD) for plans and subscriptions.
Each function is documented for clarity and maintainability.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.models.subscription import Plan, Subscription, SubscriptionStatus
from app.schemas.subscription import PlanCreate, SubscriptionCreate, SubscriptionUpdate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_plan(db: Session, plan: PlanCreate) -> Plan:
    """
    Create a new subscription plan in the database.
    """
    logger.info(f"Creating plan with name: {plan.name}")
    db_plan = Plan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    logger.info(f"Plan created with id: {db_plan.id}")
    return db_plan

def get_plans(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all subscription plans, with optional pagination.
    """
    logger.info(f"Retrieving plans with skip: {skip}, limit: {limit}")
    plans = db.query(Plan).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(plans)} plans")
    return plans

def get_plan(db: Session, plan_id: int):
    """
    Retrieve a single plan by its ID.
    """
    logger.info(f"Retrieving plan with id: {plan_id}")
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if plan:
        logger.info(f"Plan found with id: {plan_id}")
    else:
        logger.warning(f"Plan not found with id: {plan_id}")
    return plan

def create_subscription(db: Session, subscription: SubscriptionCreate) -> Subscription:
    """
    Create a new subscription for a user, setting the end date based on plan duration.
    """
    logger.info(f"Creating subscription for user: {subscription.user_id}, plan: {subscription.plan_id}")
    plan = get_plan(db, subscription.plan_id)
    if not plan:
        logger.error(f"Plan not found with id: {subscription.plan_id}")
        raise ValueError("Plan not found")
    
    end_date = datetime.utcnow() + timedelta(days=plan.duration_days)
    db_subscription = Subscription(
        **subscription.model_dump(),
        end_date=end_date
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    logger.info(f"Subscription created for user: {subscription.user_id}, subscription_id: {db_subscription.id}")
    return db_subscription

def get_user_subscription(db: Session, user_id: int):
    """
    Retrieve the active subscription for a given user.
    """
    logger.info(f"Retrieving subscription for user: {user_id}")
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == SubscriptionStatus.ACTIVE
    ).first()
    if subscription:
        logger.info(f"Subscription found for user: {user_id}, subscription_id: {subscription.id}")
    else:
        logger.warning(f"No active subscription found for user: {user_id}")
    return subscription

def update_subscription(
    db: Session, 
    user_id: int, 
    subscription_update: SubscriptionUpdate
) -> Subscription:
    """
    Update a user's active subscription (e.g., change plan or status).
    """
    logger.info(f"Updating subscription for user: {user_id}")
    subscription = get_user_subscription(db, user_id)
    if not subscription:
        logger.error(f"No active subscription found for user: {user_id}")
        raise ValueError("Active subscription not found")

    update_data = subscription_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subscription, field, value)

    if subscription_update.plan_id:
        plan = get_plan(db, subscription_update.plan_id)
        if not plan:
            logger.error(f"Plan not found with id: {subscription_update.plan_id}")
            raise ValueError("Plan not found")
        subscription.end_date = datetime.utcnow() + timedelta(days=plan.duration_days)

    db.commit()
    db.refresh(subscription)
    logger.info(f"Subscription updated for user: {user_id}, subscription_id: {subscription.id}")
    return subscription

def cancel_subscription(db: Session, user_id: int) -> Subscription:
    """
    Cancel a user's active subscription by setting its status to CANCELLED.
    """
    logger.info(f"Cancelling subscription for user: {user_id}")
    subscription = get_user_subscription(db, user_id)
    if not subscription:
        logger.error(f"No active subscription found for user: {user_id}")
        raise ValueError("Active subscription not found")

    subscription.status = SubscriptionStatus.CANCELLED
    db.commit()
    db.refresh(subscription)
    logger.info(f"Subscription cancelled for user: {user_id}, subscription_id: {subscription.id}")
    return subscription