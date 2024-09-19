import os
import PyPDF2
from src.utils.logger import log_message
from src.utils.decorators import handle_error
from config import FILES_DIR

@handle_error
def extract_text_from_pdf(pdf_filename):
    """
    Extrae texto de un archivo PDF ubicado en la carpeta 'files'.
    
    Parámetros:
    - pdf_filename: Nombre del archivo PDF del que se extraerá el texto.
    
    Retorna:
    - text: El texto extraído del PDF.
    
    Lanza:
    - RuntimeError si ocurre un error durante la lectura del PDF.
    """
    pdf_path = os.path.join(FILES_DIR, pdf_filename)
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    
    log_message(f"Texto extraído correctamente del archivo: {pdf_filename}")
    return text  # Devolver el texto extraído, no modificar el estado