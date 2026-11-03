import os

# The app requires mandatory settings at import time (app.core.config.Settings).
# Provide safe test-only values before main is imported so `pytest` works with
# zero manual configuration. Real credentials are never used here; CI and
# local runs both inherit these defaults while .env can still override them.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_local.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-not-a-real-key")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from app.db.base_class import Base
from app.db.session import get_db
from app.models.subscription import Plan, Subscription
from app.models.user import User

# Use an in-memory SQLite database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
