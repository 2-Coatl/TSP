from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_config

# Obtenemos la configuración
config = get_config()

# Creamos el engine de SQLAlchemy
engine = create_engine(config.DATABASE_URL, pool_size=5, max_overflow=10)

# Creamos una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creamos la clase Base para nuestros modelos
Base = declarative_base()

# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()