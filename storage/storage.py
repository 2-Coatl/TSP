from db import DatabaseManager
from file_system import FileSystemManager
from redis_client import RedisClient
from utils.decorators import handle_error
from utils.logger import LoggerManager
import os

class StorageService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.file_manager = FileSystemManager(os.getenv('STORAGE_PATH', '/data'))
        self.redis_client = RedisClient()

    @handle_error
    def store_document(self, file, filename, source_language, target_language):
        LoggerManager.log_message(f"Storing document: {filename}")
        file_path, file_size = self.file_manager.save_file(file, filename)
        doc_id = self.db_manager.add_document(filename, file_path, file_size, source_language, target_language)
        self.redis_client.publish('new_document', str(doc_id))
        LoggerManager.log_message(f"Document stored successfully. ID: {doc_id}")
        return doc_id

    @handle_error
    def get_document(self, doc_id):
        LoggerManager.log_message(f"Retrieving document: {doc_id}")
        doc = self.db_manager.get_document(doc_id)
        if doc:
            file_content = self.file_manager.get_file(doc.file_path)
            return {
                'id': doc.id,
                'filename': doc.filename,
                'status': doc.status,
                'content': file_content
            }
        LoggerManager.log_message(f"Document not found: {doc_id}", level='warning')
        return None

    @handle_error
    def update_document_status(self, doc_id, new_status):
        LoggerManager.log_message(f"Updating document status: {doc_id} to {new_status}")
        return self.db_manager.update_document_status(doc_id, new_status)

    @handle_error
    def get_documents_for_translation(self):
        LoggerManager.log_message("Retrieving documents for translation")
        return self.db_manager.get_documents_for_translation()