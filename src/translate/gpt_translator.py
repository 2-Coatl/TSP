import openai
from src.utils.logger import log_message, handle_error

@handle_error
def translate_text(text):
    """Traduce el texto usando la API de GPT."""
    log_message("Iniciando la traducción del texto")
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Traduce el siguiente texto al español latino:\n\n{text}",
        max_tokens=2000
    )
    log_message("Traducción completada exitosamente")
    return response.choices[0].text.strip()
