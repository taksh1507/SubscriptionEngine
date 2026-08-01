import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal
from app.models.subscription import Subscription, SubscriptionStatus

logger = logging.getLogger(__name__)

def expire_subscriptions():
    """
    Background job to check for expired subscriptions and update their status.
    Handles both normal expirations and cancel-at-period-end transitions.
    """
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        # Find subscriptions that are ACTIVE but their end_date has passed
        expired_subs = db.query(Subscription).filter(
            Subscription.status == SubscriptionStatus.ACTIVE,
            Subscription.end_date < now,
            Subscription.is_deleted == False
        ).all()

        for sub in expired_subs:
            if sub.cancel_at_period_end:
                sub.status = SubscriptionStatus.CANCELLED
                logger.info(f"Subscription {sub.id} (User {sub.user_id}) marked as CANCELLED (period ended)")
            else:
                sub.status = SubscriptionStatus.EXPIRED
                logger.info(f"Subscription {sub.id} (User {sub.user_id}) marked as EXPIRED")

        if expired_subs:
            db.commit()
            logger.info(f"Processed {len(expired_subs)} expired/cancelled subscriptions.")
    except Exception as e:
        logger.error(f"Error in expire_subscriptions job: {e}")
        db.rollback()
    finally:
        db.close()

scheduler = BackgroundScheduler()
# Run every 5 minutes for demo purposes (usually daily or hourly in production)
scheduler.add_job(expire_subscriptions, 'interval', minutes=5, id='expire_subs_job', replace_existing=True)

def start_scheduler():
    if not scheduler.running:
        logger.info("Starting background scheduler...")
        scheduler.start()

def shutdown_scheduler():
    if scheduler.running:
        logger.info("Shutting down background scheduler...")
        scheduler.shutdown()
