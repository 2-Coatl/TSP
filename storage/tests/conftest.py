import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.base import BaseManager, Base
from src.db.managers.document_manager import DocumentManager
from config import TestingConfig


@pytest.fixture(scope="session")
def app_config():
    return TestingConfig()

@pytest.fixture(scope="function")
def base_manager(app_config):
    manager = BaseManager()
    manager.config = app_config
    manager.create_tables()
    yield manager
    Base.metadata.drop_all(manager.engine)

@pytest.fixture(scope="function")
def db_session(base_manager):
    with base_manager.get_session() as session:
        yield session

@pytest.fixture(scope="function")
def doc_manager(db_engine, app_config):
    manager = DocumentManager()
    manager.engine = db_engine
    manager.SessionLocal = sessionmaker(bind=db_engine)
    Base.metadata.create_all(db_engine)
    yield manager
    Base.metadata.drop_all(db_engine)