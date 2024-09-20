from src.utils.logger import log_message
from src.utils.error_handling import handle_error
from .ITranslator import Translator

class GPTTranslator(Translator):
    """Implementación del traductor utilizando la API de GPT."""
    
    @handle_error
    def translate(self, text: str) -> str:
        """Traduce el texto usando la API de GPT.
        
        Args:
            text (str): El texto que se va a traducir.
        
        Returns:
            str: El texto traducido al español latino.
        """
        log_message("Iniciando la traducción con GPT.")
        
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=f"Traduce el siguiente texto al español latino:\n\n{text}",
            max_tokens=2000
        )
        
        log_message("Traducción completada exitosamente con GPT.")
        
        return response.choices[0].text.strip()
