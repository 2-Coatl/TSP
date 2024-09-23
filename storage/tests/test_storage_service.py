import pytest
from storage import StorageService
from db import DatabaseManager
from file_system import FileSystemManager
from redis_client import RedisClient

@pytest.fixture
def storage_service():
    # Configurar los mocks o instancias de prueba para las dependencias
    db_manager = DatabaseManager()
    file_manager = FileSystemManager("/tmp/test_storage")
    redis_client = RedisClient()
    
    # Crear una instancia de StorageService con las dependencias
    return StorageService(db_manager, file_manager, redis_client)

def test_storage_service_initialization(storage_service):
    assert storage_service is not None
    assert isinstance(storage_service, StorageService)

def test_store_document(storage_service):
    doc_id = "test_doc_1"
    content = "This is a test document"
    result = storage_service.store_document(doc_id, content)
    assert result is True
    
    # Verificar que el documento se puede recuperar
    retrieved_content = storage_service.get_document(doc_id)
    assert retrieved_content == content

def test_delete_document(storage_service):
    doc_id = "test_doc_2"
    content = "This is another test document"
    storage_service.store_document(doc_id, content)
    
    # Verificar que el documento se puede eliminar
    result = storage_service.delete_document(doc_id)
    assert result is True
    
    # Verificar que el documento ya no se puede recuperar
    with pytest.raises(Exception):  # Ajusta esto al tipo de excepción que lanzas cuando un documento no se encuentra
        storage_service.get_document(doc_id)