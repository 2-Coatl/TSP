import os
from db import DatabaseManager
from file_system import FileSystemManager
from redis_client import RedisClient
from utils.decorators import handle_error
from utils.logger import LoggerManager

class StorageService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.file_manager = FileSystemManager(os.getenv('STORAGE_PATH', '/data'))
        self.redis_client = RedisClient()

    @handle_error
    def upload_pdf(self, file, filename, source_language, target_language):
        """
        Paso 1: Subida de PDF
        """
        LoggerManager.log_message(f"Uploading PDF: {filename}")
        file_path, file_size = self.file_manager.save_file(file, filename)
        doc_id = self.db_manager.add_document(filename, file_path, file_size, source_language, target_language)
        
        # Notificar al Servicio de Traducción
        self.redis_client.publish('new_document_for_translation', str(doc_id))
        
        LoggerManager.log_message(f"PDF uploaded successfully. ID: {doc_id}")
        return doc_id

    @handle_error
    def store_translated_text(self, doc_id, translated_text):
        """
        Paso 3: Almacenamiento del Documento Traducido
        """
        LoggerManager.log_message(f"Storing translated text for document: {doc_id}")
        
        # Guardar el texto traducido
        translated_filename = f"translated_{doc_id}.txt"
        translated_path = self.file_manager.save_file(translated_text.encode(), translated_filename)
        
        # Actualizar metadatos en PostgreSQL
        self.db_manager.update_document_status(doc_id, 'translated')
        self.db_manager.update_document_translated_path(doc_id, translated_path)
        
        # Notificar al Servicio de Notificación
        self.redis_client.publish('translation_complete', str(doc_id))
        
        LoggerManager.log_message(f"Translated text stored for document: {doc_id}")

    @handle_error
    def get_document(self, doc_id):
        """
        Obtener información del documento
        """
        LoggerManager.log_message(f"Retrieving document: {doc_id}")
        doc = self.db_manager.get_document(doc_id)
        if doc:
            return {
                'id': doc.id,
                'filename': doc.filename,
                'status': doc.status,
                'source_language': doc.source_language,
                'target_language': doc.target_language
            }
        LoggerManager.log_message(f"Document not found: {doc_id}", level='warning')
        return None

    @handle_error
    def get_document_content(self, doc_id, translated=False):
        """
        Obtener el contenido del documento (original o traducido)
        """
        doc = self.db_manager.get_document(doc_id)
        if not doc:
            LoggerManager.log_message(f"Document not found: {doc_id}", level='warning')
            return None

        if translated and doc.status != 'translated':
            LoggerManager.log_message(f"Translated version not available for document: {doc_id}", level='warning')
            return None

        file_path = doc.translated_path if translated else doc.file_path
        return self.file_manager.get_file(file_path)

    @handle_error
    def get_documents_for_translation(self):
        """
        Obtener documentos pendientes de traducción
        """
        LoggerManager.log_message("Retrieving documents for translation")
        return self.db_manager.get_documents_for_translation()