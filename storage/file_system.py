import os
import shutil
from datetime import datetime
from utils.decorators import handle_error
from utils.logger import LoggerManager

class FileSystemManager:
    def __init__(self, base_path):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            LoggerManager.log_message(f"Created base path: {self.base_path}", level='info')

    @handle_error
    def save_file(self, file, filename):
        """
        Guarda un archivo en el sistema de archivos.
        
        :param file: Objeto de archivo (generalmente un objeto tipo file-like de un framework web)
        :param filename: Nombre original del archivo
        :return: (path del archivo guardado, tamaño del archivo)
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        safe_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(self.base_path, safe_filename)
        
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file, buffer)
        
        file_size = os.path.getsize(file_path)
        LoggerManager.log_message(f"File saved: {safe_filename}, Size: {file_size} bytes", level='info')
        return file_path, file_size

    @handle_error
    def get_file(self, file_path):
        """
        Recupera un archivo del sistema de archivos.
        
        :param file_path: Ruta completa al archivo
        :return: Contenido del archivo o None si no existe
        """
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                content = file.read()
            LoggerManager.log_message(f"File retrieved: {file_path}", level='info')
            return content
        else:
            LoggerManager.log_message(f"File not found: {file_path}", level='warning')
            return None

    @handle_error
    def delete_file(self, file_path):
        """
        Elimina un archivo del sistema de archivos.
        
        :param file_path: Ruta completa al archivo a eliminar
        :return: True si se eliminó correctamente, False si no existía
        """
        if os.path.exists(file_path):
            os.remove(file_path)
            LoggerManager.log_message(f"File deleted: {file_path}", level='info')
            return True
        else:
            LoggerManager.log_message(f"File not found for deletion: {file_path}", level='warning')
            return False

    @handle_error
    def list_files(self):
        """
        Lista todos los archivos en el directorio base.
        
        :return: Lista de nombres de archivo en el directorio base
        """
        files = [f for f in os.listdir(self.base_path) if os.path.isfile(os.path.join(self.base_path, f))]
        LoggerManager.log_message(f"Listed {len(files)} files in {self.base_path}", level='info')
        return files