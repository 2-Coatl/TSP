import os
import PyPDF2
from abc import ABC, abstractmethod
from src.utils.logger import LoggerManager
from src.utils.decorators import handle_error
from src.utils.config import FILES_DIR
from .interface import ITextExtractor


class PDFTextExtractor(ITextExtractor):
    @handle_error
    def extract_text(self, pdf_filename: str, start_page: int = 0, end_page: int = None) -> list:
        """
        Extrae texto de un archivo PDF ubicado en la carpeta 'files'.
        
        Parámetros:
        - pdf_filename: Nombre del archivo PDF del que se extraerá el texto.
        - start_page: Página inicial para extraer (cero-indexada).
        - end_page: Página final para extraer (cero-indexada), o None para la última página.
        
        Retorna:
        - list: Lista con el texto extraído de las páginas especificadas.
        """
        pdf_path = os.path.join(FILES_DIR, pdf_filename)
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            end_page = end_page or len(reader.pages) - 1
            extracted_texts = []
            
            for i in range(start_page, end_page + 1):
                page_text = reader.pages[i].extract_text() or ""
                extracted_texts.append(page_text)
                LoggerManager.log_message(f"Texto extraído de la página {i + 1} del archivo: {pdf_filename}", level='info')

        LoggerManager.log_message(f"Texto extraído correctamente del archivo: {pdf_filename}", level='info')
        return extracted_texts  # Devolver una lista de textos por página