import logging
import os

class LoggerManager:
    _logger = None

    @classmethod
    def setup_logger(cls, name=None, log_file=None, level=logging.INFO):
        """Configura el logger con un formato estándar."""
        if cls._logger is None:  # Evitar configurar el logger más de una vez
            if name is None:
                name = 'app_logger'
            if log_file is None:
                log_file = 'logs/app.log'  # Puede ser configurado dinámicamente

            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            cls._logger = logging.getLogger(name)
            cls._logger.setLevel(level)
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls._logger.addHandler(handler)

    @classmethod
    def log_message(cls, message, level='info'):
        cls.setup_logger()  # Se puede configurar aquí si se desea un logger predeterminado
        if level == 'info':
            cls._logger.info(message)
        elif level == 'warning':
            cls._logger.warning(message)
        elif level == 'error':
            cls._logger.error(message)
        else:
            cls._logger.debug(message)
