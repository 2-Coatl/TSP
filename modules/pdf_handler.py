import PyPDF2

def extract_text_from_pdf(pdf_path):
    """Extrae texto de un archivo PDF."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        raise RuntimeError(f"Error al leer el PDF: {str(e)}")
