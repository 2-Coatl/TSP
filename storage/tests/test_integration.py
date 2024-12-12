class TestIntegration:
    def test_full_document_workflow(self, doc_manager, app_config):
        # Add a document
        doc_id = doc_manager.add_document("integration_test.txt", f"{app_config.STORAGE_PATH}/integration_test.txt",
                                          1024, "en", "es")

        # Verify it was added correctly
        doc = doc_manager.get_document(doc_id)
        assert doc.filename == "integration_test.txt"
        assert doc.status == "uploaded"

        # Update the status
        success = doc_manager.update_document_status(doc_id, "translating")
        assert success

        # Verify the status was updated
        doc = doc_manager.get_document(doc_id)
        assert doc.status == "translating"

        # Verify it's not in the list of documents to translate
        docs_to_translate = doc_manager.get_documents_for_translation()
        assert doc_id not in [d.id for d in docs_to_translate]