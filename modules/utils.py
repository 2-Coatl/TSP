import logging
import os

def save_translation_to_file(text, output_path):
    """Guarda el texto traducido en un archivo."""
    try:
        with open(output_path, 'w') as file:
            file.write(text)
    except Exception as e:
        raise RuntimeError(f"Error al guardar el archivo: {str(e)}")

def setup_logger(name, log_file, level=logging.INFO):
    """Configura el logger con un formato estándar"""
    os.makedirs('logs', exist_ok=True)
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    handler = logging.FileHandler(log_file)
    handler.setFormatter(log_formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

# Ejemplo de uso global en otros módulos
logger = setup_logger('app_logger', 'logs/app.log')

def log_message(message, level='info'):
    """Función para loggear mensajes a lo largo del proyecto"""
    if level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
    else:
        logger.debug(message)

def handle_error(func):
    """Decorador para manejar errores de manera uniforme"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_message(f"Error en la función {func.__name__}: {str(e)}", level='error')
            raise e
    return wrapper
