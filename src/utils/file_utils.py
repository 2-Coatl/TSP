from .logger import log_message

def save_translation_to_file(text, output_path):
    """Guarda el texto traducido en un archivo."""
    try:
        with open(output_path, 'w') as file:
            file.write(text)
        log_message(f"Texto traducido guardado en {output_path}", level='info')
    except Exception as e:
        log_message(f"Error al guardar el archivo: {str(e)}", level='error')
        raise RuntimeError(f"Error al guardar el archivo: {str(e)}")
