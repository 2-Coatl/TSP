import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from utils.logger import LoggerManager
from storage import StorageService
from db import DatabaseManager
from file_system import FileSystemManager
from redis_client import RedisClient
from utils.config import REDIS_CHANNEL_NEW_DOCUMENT, REDIS_CHANNEL_TRANSLATION_COMPLETE

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Variables globales para los servicios
db_manager = None
file_manager = None
redis_client = None
storage_service = None


def initialize_services():
    """Inicializa y retorna todos los servicios necesarios."""
    global db_manager, file_manager, redis_client, storage_service
    db_manager = DatabaseManager()
    file_manager = FileSystemManager(os.getenv('STORAGE_PATH'))
    redis_client = RedisClient()
    storage_service = StorageService()
    return db_manager, file_manager, redis_client, storage_service


@app.route('/health')
def health_check():
    # Verifica que todos los servicios estén operativos
    if db_manager and file_manager and redis_client and storage_service:
        # Puedes añadir más verificaciones aquí si es necesario
        return jsonify({"status": "healthy"}), 200
    else:
        return jsonify({"status": "unhealthy"}), 500

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
    log_file = os.getenv('LOG_FILE')
    log_level = os.getenv('LOG_LEVEL')
    LoggerManager.setup_logger(name='storage_service', log_file=log_file, level=log_level)

    # Inicializar servicios
    initialize_services()

    # Crear tablas de la base de datos si no existen
    db_manager.create_tables()

    # Configurar listeners de Redis
    pubsub = setup_redis_listeners(redis_client, storage_service)

    LoggerManager.log_message("Servicio de Almacenamiento iniciado", level='info')

    # Iniciar el servidor Flask en un hilo separado
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()

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