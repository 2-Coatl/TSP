import os

# Configuración de la API
API_KEY = os.getenv('OPENAI_API_KEY', 'tu_api_key_por_defecto')

# Configuración de directorios
FILES_DIR = 'files/'
LOGS_DIR = 'logs/'

# Configuración de logging
LOG_FILE = os.path.join(LOGS_DIR, 'app.log')
