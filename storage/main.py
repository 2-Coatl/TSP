import os
from dotenv import load_dotenv
from utils.logger import LoggerManager
from storage import StorageService
from db import DatabaseManager
from file_system import FileSystemManager
from redis_client import RedisClient
from utils.config import REDIS_CHANNEL_NEW_DOCUMENT, REDIS_CHANNEL_TRANSLATION_COMPLETE

# Cargar variables de entorno
load_dotenv()

def initialize_services():
    """Inicializa y retorna todos los servicios necesarios."""
    db_manager = DatabaseManager()
    file_manager = FileSystemManager(os.getenv('STORAGE_PATH', '/data'))
    redis_client = RedisClient()
    storage_service = StorageService()
    return db_manager, file_manager, redis_client, storage_service

def setup_redis_listeners(redis_client, storage_service):
    """Configura los listeners de Redis para manejar eventos."""
    def handle_new_document(message):
        doc_id = message['data']
        LoggerManager.log_message(f"Nuevo documento recibido para traducción: {doc_id}")
        # Aquí podrías iniciar el proceso de traducción o cualquier otra lógica necesaria

    def handle_translation_complete(message):
        doc_id = message['data']
        LoggerManager.log_message(f"Traducción completada para el documento: {doc_id}")
        # Aquí podrías actualizar el estado del documento o iniciar el proceso de notificación

    pubsub = redis_client.client.pubsub()
    pubsub.subscribe(**{
        REDIS_CHANNEL_NEW_DOCUMENT: handle_new_document,
        REDIS_CHANNEL_TRANSLATION_COMPLETE: handle_translation_complete
    })
    return pubsub

def main():
    # Configurar el logger
    log_file = os.getenv('LOG_FILE', 'logs/storage_service.log')
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    LoggerManager.setup_logger(name='storage_service', log_file=log_file, level=log_level)

    # Inicializar servicios
    db_manager, file_manager, redis_client, storage_service = initialize_services()

    # Crear tablas de la base de datos si no existen
    db_manager.create_tables()

    # Configurar listeners de Redis
    pubsub = setup_redis_listeners(redis_client, storage_service)

    LoggerManager.log_message("Servicio de Almacenamiento iniciado", level='info')

    # Mantener el servicio en ejecución
    try:
        for message in pubsub.listen():
            if message['type'] == 'message':
                # El manejo de mensajes se realiza en las funciones de callback
                pass
    except KeyboardInterrupt:
        LoggerManager.log_message("Servicio de Almacenamiento detenido", level='info')
    finally:
        pubsub.close()

if __name__ == "__main__":
    main()