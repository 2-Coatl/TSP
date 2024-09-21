import os
import shutil
from datetime import datetime
from utils.decorators import handle_error
from utils.logger import LoggerManager
from io import BytesIO

class FileSystemManager:
    def __init__(self, base_path):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            LoggerManager.log_message(f"Created base path: {self.base_path}", level='info')

    def _get_directory_path(self, date=None):
        """
        Genera la ruta del directorio basada en la fecha.
        
        :param date: Fecha para la cual generar la ruta (default: fecha actual)
        :return: Ruta del directorio
        """
        if date is None:
            date = datetime.now()
        return os.path.join(self.base_path, date.strftime("%Y"), date.strftime("%m"), date.strftime("%d"))

    @handle_error
    def save_file(self, file_or_content, filename):
        """
        Guarda un archivo o contenido en el sistema de archivos.
        
        :param file_or_content: Objeto de archivo, bytes, o string a guardar
        :param filename: Nombre del archivo
        :return: (path del archivo guardado, tamaño del archivo)
        """
        timestamp = datetime.now()
        dir_path = self._get_directory_path(timestamp)
        os.makedirs(dir_path, exist_ok=True)
        
        safe_filename = f"{timestamp.strftime('%H%M%S')}_{filename}"
        file_path = os.path.join(dir_path, safe_filename)
        
        if isinstance(file_or_content, (str, bytes)):
            mode = 'w' if isinstance(file_or_content, str) else 'wb'
            with open(file_path, mode) as f:
                f.write(file_or_content)
        elif hasattr(file_or_content, 'read'):
            with open(file_path, 'wb') as buffer:
                shutil.copyfileobj(file_or_content, buffer)
        else:
            raise ValueError("Unsupported file or content type")
        
        file_size = os.path.getsize(file_path)
        LoggerManager.log_message(f"File saved: {file_path}, Size: {file_size} bytes", level='info')
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
            # Intentar eliminar directorios vacíos
            self._cleanup_empty_dirs(os.path.dirname(file_path))
            return True
        else:
            LoggerManager.log_message(f"File not found for deletion: {file_path}", level='warning')
            return False

    @handle_error
    def list_files(self, date=None):
        """
        Lista todos los archivos en el directorio especificado por la fecha.
        
        :param date: Fecha para la cual listar los archivos (default: fecha actual)
        :return: Lista de rutas completas de archivos en el directorio
        """
        dir_path = self._get_directory_path(date)
        if os.path.exists(dir_path):
            files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
            LoggerManager.log_message(f"Listed {len(files)} files in {dir_path}", level='info')
            return files
        else:
            LoggerManager.log_message(f"Directory not found: {dir_path}", level='warning')
            return []

    @handle_error
    def get_file_size(self, file_path):
        """
        Obtiene el tamaño de un archivo.
        
        :param file_path: Ruta completa al archivo
        :return: Tamaño del archivo en bytes, o None si el archivo no existe
        """
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            LoggerManager.log_message(f"File size retrieved for {file_path}: {size} bytes", level='info')
            return size
        else:
            LoggerManager.log_message(f"File not found for size retrieval: {file_path}", level='warning')
            return None

    def _cleanup_empty_dirs(self, path):
        """
        Elimina directorios vacíos recursivamente.
        
        :param path: Ruta del directorio a verificar
        """
        if not os.path.isdir(path):
            return

        # Eliminar subdirectorios vacíos
        for subdir in os.listdir(path):
            subdir_path = os.path.join(path, subdir)
            if os.path.isdir(subdir_path):
                self._cleanup_empty_dirs(subdir_path)

        # Intentar eliminar el directorio actual si está vacío
        if not os.listdir(path):
            os.rmdir(path)
            LoggerManager.log_message(f"Removed empty directory: {path}", level='info')