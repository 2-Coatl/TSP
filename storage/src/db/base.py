from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config import get_config
from sqlalchemy.pool import QueuePool

Base = declarative_base()

class BaseManager:
    def __init__(self):
        self.config = get_config()
        self.engine = create_engine(
            self.config.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

# Función de utilidad para obtener una sesión de base de datos
def get_db():
    manager = BaseManager()
    with manager.get_session() as session:
        yield session