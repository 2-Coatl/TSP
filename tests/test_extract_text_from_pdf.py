import os
import pytest
from unittest import mock
from src.utils.pdf_handler import extract_text_from_pdf  # Asumimos que está en pdf_handler.py

# Setup para los archivos de prueba
FILES_DIR = 'files'
TEST_PDF_FILE = 'test_pdf.pdf'
TEST_NON_EXISTENT_FILE = 'non_existent_file.pdf'

# Simulamos el contenido de un archivo PDF (puedes crear un mock para PyPDF2)
mock_pdf_content = "Este es el texto de prueba en el PDF."

# Mock para PyPDF2
class MockPdfReader:
    def __init__(self, file):
        self.pages = [self]

    def extract_text(self):
        return mock_pdf_content

# Test para asegurar que el texto se extrae correctamente de un PDF
@mock.patch("PyPDF2.PdfReader", return_value=MockPdfReader(None))
def test_extract_text_from_pdf_success(mock_reader):
    # Path del archivo de prueba
    test_pdf_path = os.path.join(FILES_DIR, TEST_PDF_FILE)

    # Simular la existencia del archivo en el sistema
    with mock.patch("builtins.open", mock.mock_open(read_data="data")):
        extracted_text = extract_text_from_pdf(TEST_PDF_FILE)

    assert extracted_text == mock_pdf_content, "El texto extraído no coincide con el contenido esperado"
    
# Test para manejar un archivo que no existe
def test_extract_text_from_pdf_file_not_found():
    # Asegurar que se lanza una excepción si el archivo no existe
    with pytest.raises(RuntimeError, match="Error al leer el PDF"):
        extract_text_from_pdf(TEST_NON_EXISTENT_FILE)
