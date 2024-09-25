import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.base import Base
from src.db.managers.document_manager import DocumentManager
from config import TestingConfig

@pytest.fixture(scope="session")
def app_config():
    return TestingConfig()

@pytest.fixture(scope="session")
def db_engine(app_config):
    return create_engine(app_config.DATABASE_URL)

@pytest.fixture(scope="function")
def db_session(db_engine):
    Base.metadata.create_all(db_engine)
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(db_engine)

@pytest.fixture(scope="function")
def doc_manager(db_engine, app_config):
    manager = DocumentManager()
    manager.engine = db_engine
    manager.SessionLocal = sessionmaker(bind=db_engine)
    Base.metadata.create_all(db_engine)
    yield manager
    Base.metadata.drop_all(db_engine)