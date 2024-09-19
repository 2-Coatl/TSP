def save_translation_to_file(text, output_path):
    """Guarda el texto traducido en un archivo."""
    try:
        with open(output_path, 'w') as file:
            file.write(text)
    except Exception as e:
        raise RuntimeError(f"Error al guardar el archivo: {str(e)}")
