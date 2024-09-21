import os
from db import DatabaseManager
from file_system import FileSystemManager
from redis_client import RedisClient
from utils.decorators import handle_error
from utils.logger import LoggerManager
from utils.config import REDIS_CHANNEL_NEW_DOCUMENT, REDIS_CHANNEL_TRANSLATION_COMPLETE

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
        self.redis_client.publish(REDIS_CHANNEL_NEW_DOCUMENT, str(doc_id))
        
        LoggerManager.log_message(f"PDF uploaded successfully. ID: {doc_id}")
        return doc_id

    @handle_error
    def store_translated_text(self, doc_id, translated_text):
        """
        Paso 3: Almacenamiento del Documento Traducido
        """
        LoggerManager.log_message(f"Storing translated text for document: {doc_id}")
        
        # Obtener el documento original
        original_doc = self.db_manager.get_document(doc_id)
        if not original_doc:
            raise ValueError(f"Document with ID {doc_id} not found")
        
        # Guardar el texto traducido
        translated_filename = f"translated_{os.path.basename(original_doc.file_path)}"
        translated_path, _ = self.file_manager.save_file(translated_text, translated_filename)
        
        # Actualizar metadatos en PostgreSQL
        self.db_manager.update_document_translated_path(doc_id, translated_path)
        
        # Notificar al Servicio de Notificación
        self.redis_client.publish(REDIS_CHANNEL_TRANSLATION_COMPLETE, str(doc_id))
        
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
                'file_path': doc.file_path,
                'translated_path': doc.translated_path,
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

        if translated and not doc.translated_path:
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
