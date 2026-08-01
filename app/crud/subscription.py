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
    try:
        logger.info(f"Creating plan with name: {plan.name}")
        db_plan = Plan(**plan.model_dump())
        db.add(db_plan)
        db.commit()
        db.refresh(db_plan)
        logger.info(f"Plan created with id: {db_plan.id}")
        return db_plan
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating plan: {e}")
        raise ValueError("Failed to create plan")

def get_plans(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all subscription plans, with optional pagination.
    """
    logger.info(f"Retrieving plans with skip: {skip}, limit: {limit}")
    total = db.query(Plan).filter(Plan.is_deleted == False).count()
    plans = db.query(Plan).filter(Plan.is_deleted == False).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(plans)} plans out of {total}")
    return plans, total

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
    
    try:
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
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating subscription: {e}")
        raise ValueError(str(e))

def get_user_subscription(db: Session, user_id: int):
    """
    Retrieve the active subscription for a given user.
    """
    logger.info(f"Retrieving subscription for user: {user_id}")
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.status == SubscriptionStatus.ACTIVE,
        Subscription.is_deleted == False
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

    try:
        update_data = subscription_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(subscription, field, value)

        if subscription_update.plan_id:
            plan = get_plan(db, subscription_update.plan_id)
            if not plan:
                logger.error(f"Plan not found with id: {subscription_update.plan_id}")
                raise ValueError("Plan not found")
            # Upgrade/downgrade resets the billing cycle to today
            subscription.start_date = datetime.utcnow()
            subscription.end_date = datetime.utcnow() + timedelta(days=plan.duration_days)

        db.commit()
        db.refresh(subscription)
        logger.info(f"Subscription updated for user: {user_id}, subscription_id: {subscription.id}")
        return subscription
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating subscription: {e}")
        raise ValueError(str(e))

def cancel_subscription(db: Session, user_id: int) -> Subscription:
    """
    Cancel a user's active subscription by setting its cancel_at_period_end flag to True.
    """
    logger.info(f"Cancelling subscription for user: {user_id}")
    subscription = get_user_subscription(db, user_id)
    if not subscription:
        logger.error(f"No active subscription found for user: {user_id}")
        raise ValueError("Active subscription not found")

    try:
        subscription.cancel_at_period_end = True
        db.commit()
        db.refresh(subscription)
        logger.info(f"Subscription cancelled at period end for user: {user_id}, subscription_id: {subscription.id}")
        return subscription
    except Exception as e:
        db.rollback()
        logger.error(f"Error cancelling subscription: {e}")
        raise ValueError(str(e))