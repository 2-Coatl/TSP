import os
from typing import List

class Config:
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING: bool = os.getenv('TESTING', 'False').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'default-secret-key')

    # Database configuration
    DB_HOST: str = os.getenv('DB_HOST', 'db')
    DB_NAME: str = os.getenv('DB_NAME', 'pdf_translation_db')
    DB_USER: str = os.getenv('DB_USER', 'pdf_translator')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'secure_password')

    # Redis configuration
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB: int = int(os.getenv('REDIS_DB', 0))

    # Storage configuration
    STORAGE_PATH: str = os.getenv('STORAGE_PATH', '/data')
    MAX_UPLOAD_SIZE: int = int(os.getenv('MAX_UPLOAD_SIZE', 20971520))
    ALLOWED_FILE_TYPES: List[str] = os.getenv('ALLOWED_FILE_TYPES', 'pdf,docx,txt,png').split(',')

    # Logging configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'DEBUG')
    LOG_FILE_STORAGE: str = os.getenv('LOG_FILE_STORAGE', '/app/logs/storage_service.log')

    # OpenAI configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')

    # Notification configuration
    NOTIFICATION_TYPE: str = os.getenv('NOTIFICATION_TYPE', 'email')

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @classmethod
    def get_config(cls):
        return cls()

# Configuraciones específicas para diferentes ambientes
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Elegir configuración basada en el ambiente
def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig()
    return DevelopmentConfig()


class TestingConfig(Config):
    TESTING = True
    DB_NAME = 'test_pdf_translation_db'