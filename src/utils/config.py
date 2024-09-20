import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        # Cargar variables de entorno desde un archivo .env
        load_dotenv()
        
        # Configuración de la API
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # Configuración de directorios
        self.files_dir = os.getenv('FILES_DIR')
        self.logs_dir = os.getenv('LOGS_DIR')
    
        os.makedirs(self.logs_dir, exist_ok=True)  # Crear el directorio si no existe
        self.log_file = os.path.join(self.logs_dir, 'app.log')
        
        # Otras configuraciones
        self.app_name = os.getenv("APP_NAME")
        self.environment = os.getenv("ENVIRONMENT")

    
    def __repr__(self):
        return (f"Settings(app_name={self.app_name},")

# Ejemplo de uso
if __name__ == "__main__":
    settings = Settings()
    print(settings)
