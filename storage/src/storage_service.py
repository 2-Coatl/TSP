from db.managers.document_manager import DocumentManager
from utils.logger import LoggerManager
from ..config import Config

class StorageService:
    def __init__(self):
        self.config = Config()
        self.doc_manager = DocumentManager()
        self.logger = LoggerManager(__name__)

    def initialize_database(self):
        try:
            self.doc_manager.create_tables()
            self.logger.log_message("Database tables created successfully", level='info')
        except Exception as e:
            self.logger.log_message(f"Error creating database tables: {str(e)}", level='error')
            raise

    def add_new_document(self, filename, file_path, file_size, source_language, target_language):
        try:
            doc_id = self.doc_manager.add_document(filename, file_path, file_size, source_language, target_language)
            self.logger.log_message(f"New document added with ID: {doc_id}", level='info')
            return doc_id
        except Exception as e:
            self.logger.log_message(f"Error adding new document: {str(e)}", level='error')
            raise

    def get_document(self, doc_id):
        try:
            document = self.doc_manager.get_document(doc_id)
            if document:
                self.logger.log_message(f"Retrieved document with ID: {doc_id}", level='info')
            else:
                self.logger.log_message(f"Document with ID {doc_id} not found", level='warning')
            return document
        except Exception as e:
            self.logger.log_message(f"Error retrieving document: {str(e)}", level='error')
            raise

    def update_document_status(self, doc_id, new_status):
        try:
            success = self.doc_manager.update_document_status(doc_id, new_status)
            if success:
                self.logger.log_message(f"Updated status of document {doc_id} to {new_status}", level='info')
            else:
                self.logger.log_message(f"Failed to update status of document {doc_id}", level='warning')
            return success
        except Exception as e:
            self.logger.log_message(f"Error updating document status: {str(e)}", level='error')
            raise

    def get_documents_for_translation(self, limit=10, offset=0):
        try:
            docs = self.doc_manager.get_documents_for_translation(limit, offset)
            self.logger.log_message(f"Retrieved {len(docs)} documents for translation", level='info')
            return docs
        except Exception as e:
            self.logger.log_message(f"Error retrieving documents for translation: {str(e)}", level='error')
            raise

# Example usage
if __name__ == "__main__":
    storage_service = StorageService()
    storage_service.initialize_database()

    # Add a new document
    doc_id = storage_service.add_new_document("example.txt", "/path/to/file", 1024, "en", "es")

    # Retrieve the document
    document = storage_service.get_document(doc_id)

    # Update document status
    storage_service.update_document_status(doc_id, "translating")

    # Get documents for translation
    docs_to_translate = storage_service.get_documents_for_translation(limit=10, offset=0)