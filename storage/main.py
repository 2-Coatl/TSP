import os
from utils.logger import LoggerManager
from storage import StorageService
from db import DatabaseManager

def main():
    # Configurar el logger
    log_file = os.getenv('LOG_FILE', 'logs/storage_service.log')
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    LoggerManager.setup_logger(name='storage_service', log_file=log_file, level=log_level)

    # Inicializar y configurar componentes
    db_manager = DatabaseManager()
    db_manager.create_tables()  # Asegurar que las tablas estén creadas

    # Inicializar el servicio de almacenamiento
    storage_service = StorageService()

    # Aquí puedes agregar la lógica principal de tu aplicación
    # Por ejemplo, iniciar un servidor web, procesar tareas en segundo plano, etc.
    LoggerManager.log_message("Storage Service iniciado correctamente", level='info')

if __name__ == "__main__":
    main()