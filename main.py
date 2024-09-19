from modules.pdf_handler import extract_text_from_pdf
from modules.translator import translate_text
from modules.utils import save_translation_to_file

def translate_pdf(pdf_path, output_path):
    text = extract_text_from_pdf(pdf_path)
    translation = translate_text(text)
    save_translation_to_file(translation, output_path)

if __name__ == '__main__':
    pdf_path = 'ruta_al_pdf.pdf'
    output_path = 'output/translation.txt'
    translate_pdf(pdf_path, output_path)
    print(f"Traducción guardada en: {output_path}")
