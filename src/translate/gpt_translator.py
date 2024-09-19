import openai
from src.utils.logger import log_message
from src.utils.error_handling import handle_error


@handle_error
def translate_text(text):
    """Función pura que traduce el texto sin modificar el estado original."""
    log_message("Iniciando la traducción del texto")
    
    # Llamada a la API de OpenAI
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Traduce el siguiente texto al español latino:\n\n{text}",
        max_tokens=2000
    )
    
    log_message("Traducción completada exitosamente")
    
    # Devuelve la traducción sin modificar el estado original
    return response.choices[0].text.strip()
