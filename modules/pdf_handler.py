from modules.utils import log_message
from config import FILES_DIR
import os
import PyPDF2

def extract_text_from_pdf(pdf_filename):
    """Extrae texto de un archivo PDF ubicado en la carpeta files."""
    pdf_path = os.path.join(FILES_DIR, pdf_filename)
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        log_message(f"Texto extraído correctamente del archivo: {pdf_filename}")
        return text
    except Exception as e:
        log_message(f"Error al leer el PDF: {str(e)}", level='error')
        raise RuntimeError(f"Error al leer el PDF: {str(e)}")
