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