"""
session.py
----------
Manages the SQLAlchemy database engine and session.
Provides a dependency for database access in FastAPI endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine using the database URL from settings
logger.info(f"Creating engine with URL: {settings.DATABASE_URL}")
engine = create_engine(settings.DATABASE_URL)
logger.info("Engine created")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency for getting a database session.
    Yields a session and ensures it is closed after use.
    """
    logger.info("Getting database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.info("Closing database session")