import pytest
from src.db.managers.document_manager import DocumentManager
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch, MagicMock

@pytest.fixture
def doc_manager(base_manager):
    return DocumentManager()

class TestDocumentManager:

    def test_add_document(self, doc_manager):
        doc_id = doc_manager.add_document("test.txt", "/path/to/test.txt", 1024, "en", "es")
        assert doc_id is not None
        doc = doc_manager.get_document(doc_id)
        assert doc['filename'] == "test.txt"
        assert doc['status'] == "uploaded"

    def test_get_document(self, doc_manager):
        doc_id = doc_manager.add_document("test.txt", "/path/to/test.txt", 1024, "en", "es")
        doc = doc_manager.get_document(doc_id)
        assert doc is not None
        assert doc['filename'] == "test.txt"

    def test_get_nonexistent_document(self, doc_manager):
        doc = doc_manager.get_document(999)
        assert doc is None

    def test_update_document_status(self, doc_manager):
        doc_id = doc_manager.add_document("test.txt", "/path/to/test.txt", 1024, "en", "es")
        success = doc_manager.update_document_status(doc_id, "translating")
        assert success
        doc = doc_manager.get_document(doc_id)
        assert doc['status'] == "translating"

    def test_update_nonexistent_document_status(self, doc_manager):
        success = doc_manager.update_document_status(999, "translating")
        assert not success

    def test_update_document_translated_path(self, doc_manager):
        doc_id = doc_manager.add_document("test.txt", "/path/to/test.txt", 1024, "en", "es")
        success = doc_manager.update_document_translated_path(doc_id, "/path/to/translated.txt")
        assert success
        doc = doc_manager.get_document(doc_id)
        assert doc['translated_path'] == "/path/to/translated.txt"
        assert doc['status'] == "translated"

    def test_get_documents_for_translation(self, doc_manager):
        doc_manager.add_document("test1.txt", "/path/to/test1.txt", 1024, "en", "es")
        doc_manager.add_document("test2.txt", "/path/to/test2.txt", 2048, "en", "fr")
        docs = doc_manager.get_documents_for_translation()
        assert len(docs) == 2
        assert all(doc['status'] == "uploaded" for doc in docs)

    def test_get_documents_for_translation_with_pagination(self, doc_manager):
        for i in range(5):
            doc_manager.add_document(f"test{i}.txt", f"/path/to/test{i}.txt", 1024, "en", "es")
        docs = doc_manager.get_documents_for_translation(limit=2, offset=1)
        assert len(docs) == 2
        assert docs[0]['filename'] == "test1.txt"
        assert docs[1]['filename'] == "test2.txt"

    def test_delete_document(self, doc_manager):
        doc_id = doc_manager.add_document("test.txt", "/path/to/test.txt", 1024, "en", "es")
        success = doc_manager.delete_document(doc_id)
        assert success
        doc = doc_manager.get_document(doc_id)
        assert doc is None

    def test_delete_nonexistent_document(self, doc_manager):
        success = doc_manager.delete_document(999)
        assert not success

    @patch('db.managers.document_manager.LoggerManager')
    def test_add_document_logs_error(self, mock_logger, doc_manager):
        with patch.object(doc_manager, 'get_session', side_effect=SQLAlchemyError("Test error")):
            with pytest.raises(SQLAlchemyError):
                doc_manager.add_document("test.txt", "/path/to/test.txt", 1024, "en", "es")
            mock_logger.log_message.assert_called_with("Error adding document to database: Test error", level='error')

    @patch('db.managers.document_manager.LoggerManager')
    def test_get_document_logs_error(self, mock_logger, doc_manager):
        with patch.object(doc_manager, 'get_session', side_effect=SQLAlchemyError("Test error")):
            with pytest.raises(SQLAlchemyError):
                doc_manager.get_document(1)
            mock_logger.log_message.assert_called_with("Error retrieving document: Test error", level='error')