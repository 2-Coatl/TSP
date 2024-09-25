import pytest
from src.db.models.document import Document

class TestDocumentManager:
    def test_add_document(self, doc_manager, app_config):
        doc_id = doc_manager.add_document("test.txt", f"{app_config.STORAGE_PATH}/test.txt", 1024, "en", "es")
        assert doc_id is not None
        doc = doc_manager.get_document(doc_id)
        assert doc.filename == "test.txt"
        assert doc.status == "uploaded"

    def test_get_document(self, doc_manager, app_config):
        doc_id = doc_manager.add_document("test.txt", f"{app_config.STORAGE_PATH}/test.txt", 1024, "en", "es")
        doc = doc_manager.get_document(doc_id)
        assert doc is not None
        assert doc.filename == "test.txt"

    def test_update_document_status(self, doc_manager, app_config):
        doc_id = doc_manager.add_document("test.txt", f"{app_config.STORAGE_PATH}/test.txt", 1024, "en", "es")
        success = doc_manager.update_document_status(doc_id, "translating")
        assert success
        doc = doc_manager.get_document(doc_id)
        assert doc.status == "translating"

    def test_get_documents_for_translation(self, doc_manager, app_config):
        doc_manager.add_document("test1.txt", f"{app_config.STORAGE_PATH}/test1.txt", 1024, "en", "es")
        doc_manager.add_document("test2.txt", f"{app_config.STORAGE_PATH}/test2.txt", 2048, "en", "fr")
        docs = doc_manager.get_documents_for_translation()
        assert len(docs) == 2
        assert all(doc.status == "uploaded" for doc in docs)

    def test_file_size_limit(self, doc_manager, app_config):
        with pytest.raises(ValueError):
            doc_manager.add_document("large.txt", f"{app_config.STORAGE_PATH}/large.txt",
                                     app_config.MAX_UPLOAD_SIZE + 1, "en", "es")

    def test_allowed_file_types(self, doc_manager, app_config):
        allowed_extension = app_config.ALLOWED_FILE_TYPES[0]
        not_allowed_extension = "xyz"

        # This should work
        doc_id = doc_manager.add_document(f"test.{allowed_extension}",
                                          f"{app_config.STORAGE_PATH}/test.{allowed_extension}", 1024, "en", "es")
        assert doc_id is not None

        # This should raise an error
        with pytest.raises(ValueError):
            doc_manager.add_document(f"test.{not_allowed_extension}",
                                     f"{app_config.STORAGE_PATH}/test.{not_allowed_extension}", 1024, "en", "es")


