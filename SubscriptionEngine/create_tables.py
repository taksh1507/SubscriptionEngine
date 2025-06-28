"""
create_tables.py
----------------
Script to create all database tables using SQLAlchemy models.
Run this file once after configuring your database.
"""
import logging

from app.db.session import engine
from app.models.subscription import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Creating tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created successfully.")
    print("Tables created successfully.")