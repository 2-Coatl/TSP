from abc import ABC, abstractmethod

class ITextExtractor(ABC):
    """Interfaz para un extractor de texto."""
    
    @abstractmethod
    def extract_text(self, pdf_path: str, start_page: int = 0, end_page: int = None) -> list:
        """Extrae texto de un archivo PDF.
        
        Args:
            pdf_path (str): Ruta del archivo PDF.
            start_page (int): Página de inicio.
            end_page (int): Página final.
        
        Returns:
            list: Lista de textos extraídos de las páginas especificadas.
        """
        pass
