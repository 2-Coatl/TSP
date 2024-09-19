from src.extract.pdf_extractor import extract_text_from_pdf
from src.translate.gpt_translator import translate_text
from src.utils.file_utils import save_translation_to_file
from src.utils.config import LOG_FILE, LOGS_DIR
from src.utils.logger import log_message


def main():
    logger = setup_logger('app_logger', LOGS_DIR/LOG_FILE)
    log_message("Iniciando la aplicación", level='info')
    
    # Ejemplo de archivo PDF
    pdf_filename = 'sample1.pdf'
    extracted_text = extract_text_from_pdf(pdf_filename)
    
    translated_text = translate_text(extracted_text)
    save_translation_to_file(translated_text, 'translated_output.txt')

if __name__ == "__main__":
    main()
