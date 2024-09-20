from src.extract.pdf_extractor import extract_text_from_pdf
from src.translators.gpt_translator import GPTTranslator
from src.utils.file_utils import save_translation_to_file
from src.utils.config import LOG_FILE, LOGS_DIR, FILES_DIR
from src.utils.logger import log_message


def main():
    logger = setup_logger('app_logger', LOGS_DIR/LOG_FILE)
    log_message("Iniciando la aplicación", level='info')
    
    # Crear una instancia del traductor
    translator = GPTTranslator()  # Se puede cambiar a cualquier otra implementación de Translator en el futuro

    # Ejemplo de archivo PDF
    pdf_filename = FILES_DIR/'sample1.pdf'

    # Extraer texto del PDF
    try:
        text_to_translate = extract_text_from_pdf(pdf_filename)
        print(f"Texto extraído del PDF: {text_to_translate}")
        
        # Traducir el texto extraído
        translated_text = translator.translate(text_to_translate)
        print(f"Texto traducido: {translated_text}")
        save_translation_to_file(translated_text, 'translated_output.txt')
    except RuntimeError as e:
        print(f"Ocurrió un error: {e}")
    

if __name__ == "__main__":
    main()
