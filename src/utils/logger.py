import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Configura el logger con un formato estándar."""
    os.makedirs('logs', exist_ok=True)
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    handler = logging.FileHandler(log_file)
    handler.setFormatter(log_formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

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

