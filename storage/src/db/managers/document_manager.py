from ..base import BaseManager
from ..models.document import Document
from sqlalchemy.exc import SQLAlchemyError
from ...utils.logger import LoggerManager

class DocumentManager(BaseManager):
    def add_document(self, filename, file_path, file_size, source_language, target_language):
        try:
            with self.get_session() as session:
                new_doc = Document(
                    filename=filename,
                    file_path=file_path,
                    file_size=file_size,
                    source_language=source_language,
                    target_language=target_language
                )
                session.add(new_doc)
                session.flush()
                LoggerManager.log_message(f"Document added to database: {filename}", level='info')
                return new_doc.id
        except SQLAlchemyError as e:
            LoggerManager.log_message(f"Error adding document to database: {str(e)}", level='error')
            raise

    def get_document(self, doc_id):
        try:
            with self.get_session() as session:
                doc = session.query(Document).filter(Document.id == doc_id).first()
                if doc:
                    LoggerManager.log_message(f"Retrieved document: {doc_id}", level='info')
                    return doc.to_dict()
                else:
                    LoggerManager.log_message(f"Document not found: {doc_id}", level='warning')
                    return None
        except SQLAlchemyError as e:
            LoggerManager.log_message(f"Error retrieving document: {str(e)}", level='error')
            raise

    def update_document_status(self, doc_id, new_status):
        try:
            with self.get_session() as session:
                doc = session.query(Document).filter(Document.id == doc_id).first()
                if doc:
                    doc.status = new_status
                    LoggerManager.log_message(f"Updated document status: {doc_id} to {new_status}", level='info')
                    return True
                LoggerManager.log_message(f"Failed to update document status: {doc_id}", level='warning')
                return False
        except SQLAlchemyError as e:
            LoggerManager.log_message(f"Error updating document status: {str(e)}", level='error')
            raise

    def update_document_translated_path(self, doc_id, translated_path):
        try:
            with self.get_session() as session:
                doc = session.query(Document).filter(Document.id == doc_id).first()
                if doc:
                    doc.translated_path = translated_path
                    doc.status = 'translated'
                    LoggerManager.log_message(f"Updated translated path for document: {doc_id}", level='info')
                    return True
                LoggerManager.log_message(f"Failed to update translated path for document: {doc_id}", level='warning')
                return False
        except SQLAlchemyError as e:
            LoggerManager.log_message(f"Error updating translated path: {str(e)}", level='error')
            raise

    def get_documents_for_translation(self, limit=100, offset=0):
        try:
            with self.get_session() as session:
                docs = session.query(Document).filter(Document.status == 'uploaded').limit(limit).offset(offset).all()
                LoggerManager.log_message(f"Retrieved {len(docs)} documents for translation", level='info')
                return [doc.to_dict() for doc in docs]
        except SQLAlchemyError as e:
            LoggerManager.log_message(f"Error retrieving documents for translation: {str(e)}", level='error')
            raise

    def delete_document(self, doc_id):
        try:
            with self.get_session() as session:
                doc = session.query(Document).filter(Document.id == doc_id).first()
                if doc:
                    session.delete(doc)
                    LoggerManager.log_message(f"Deleted document: {doc_id}", level='info')
                    return True
                LoggerManager.log_message(f"Failed to delete document: {doc_id}", level='warning')
                return False
        except SQLAlchemyError as e:
            LoggerManager.log_message(f"Error deleting document: {str(e)}", level='error')
            raise