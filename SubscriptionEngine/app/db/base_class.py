"""
base_class.py
-------------
Defines a base class for all SQLAlchemy models.
Automatically generates __tablename__ for each model.
"""

from typing import Any
import logging
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        logger.info(f"Generating table name for class: {cls.__name__}")
        return cls.__name__.lower()