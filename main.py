from modules.pdf_handler import extract_text_from_pdf
from modules.translator import translate_text
from modules.utils import save_translation_to_file
from src.utils.config import LOG_FILE, LOGS_DIR


if __name__ == '__main__':
    pdf_path = 'ruta_al_pdf.pdf'
    output_path = 'output/translation.txt'
    translate_pdf(pdf_path, output_path)
    print(f"Traducción guardada en: {output_path}")

logger = setup_logger('app_logger', LOGS_DIR/LOG_FILE)
