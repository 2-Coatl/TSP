from src.extract.pdf_extractor import extract_text_from_pdf
from src.translators.gpt_translator import GPTTranslator
from src.utils.file_utils import save_translation_to_file
from src.utils.config import LOG_FILE, LOGS_DIR, FILES_DIR
from src.utils.logger import log_message


def main():
    # Configurar el logger
    logger = LoggerManager('app_logger', 'logs/app.log')

    # Clave API para el traductor
    api_key = 'YOUR_OPENAI_API_KEY'
    translator = GPTTranslator(api_key)

    # Crear una instancia del extractor
    pdf_extractor = PDFTextExtractor()

    # Definir el nombre del archivo PDF y las páginas a extraer
    pdf_filename = 'example.pdf'
    start_page = 0
    end_page = None  # Extraer hasta la última página

    # Extraer texto del PDF
    extracted_texts = pdf_extractor.extract_text(pdf_filename, start_page, end_page)

    # Traducir cada texto extraído
    for page_number, text in enumerate(extracted_texts, start=start_page):
        if text.strip():  # Verificar que el texto no esté vacío
            translated_text = translator.translate(text)
            LoggerManager.log_message(f"Texto traducido de la página {page_number + 1}: {translated_text}", level='info')

    LoggerManager.log_message("Proceso de extracción y traducción completado.", level='info')

if __name__ == '__main__':
    main()
