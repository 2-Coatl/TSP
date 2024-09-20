import requests
import json
import openai
from src.utils.logger import LoggerManager
from src.utils.error_handling import handle_error
from .interface import ITranslator

class GPTTranslator(ITranslator):
    """Implementación del traductor utilizando la API de GPT."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key  # Configura la clave API de OpenAI

    @handle_error
    def translate(self, text: str) -> str:
        """Traduce el texto usando la API de GPT.
        
        Args:
            text (str): El texto que se va a traducir.
        
        Returns:
            str: El texto traducido al español latino.
        """
        LoggerManager.log_message("Iniciando la traducción con GPT.")
        
        try:
            # Aquí llamamos a la función de traducción
            translated_text = self._translate_text(text)
            LoggerManager.log_message(f"Traducción completada exitosamente con GPT.", level='info')
            return translated_text
            
        except Exception as e:
            LoggerManager.log_message(f"Error durante la traducción: {e}", level='error')
            return "Error en la traducción"  # O maneja el error como prefieras

    def _translate_text(self, text: str) -> str:
        """Realiza la traducción utilizando la API de OpenAI.

        Args:
            text (str): El texto que se va a traducir.

        Returns:
            str: El texto traducido.
        """
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un traductor profesional."
                },
                {
                    "role": "user",
                    "content": f"Traduce el siguiente texto al español latino:\n\n{text}"
                }
            ],
            "max_tokens": 2000
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        
        if response.status_code == 200:
            return response_data["choices"][0]["message"]["content"].strip()
        else:
            LoggerManager.log_message(f"Error en la API de OpenAI: {response_data.get('error', 'Error desconocido')}", level='error')
            raise Exception("Error en la API de traducción")
