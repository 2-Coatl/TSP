import pytest
from unittest import mock
from src.utils.translation import translate_text  # Asumimos que la función está en translation.py

# Mock de la respuesta de OpenAI
mock_gpt_response = {
    "choices": [
        {
            "text": "Este es el texto traducido."
        }
    ]
}

# Test para asegurar que el texto se traduce correctamente usando la API de OpenAI
@mock.patch("openai.Completion.create")
def test_translate_text_success(mock_create):
    # Simular la respuesta de la API de OpenAI
    mock_create.return_value = mock_gpt_response
    
    # Texto de prueba en inglés
    input_text = "This is a test text."
    
    # Llamada a la función
    translated_text = translate_text(input_text)
    
    # Verificar que la función devuelve la traducción correcta
    assert translated_text == "Este es el texto traducido.", "La traducción no es la esperada"
    
    # Verificar que la API fue llamada con los parámetros correctos
    mock_create.assert_called_once_with(
        engine="gpt-4",
        prompt=f"Traduce el siguiente texto al español latino:\n\n{input_text}",
        max_tokens=2000
    )

# Test para manejar errores en la llamada a la API de OpenAI
@mock.patch("openai.Completion.create", side_effect=Exception("API Error"))
def test_translate_text_api_error(mock_create):
    # Texto de prueba en inglés
    input_text = "This is a test text."
    
    # Asegurar que se lanza una excepción si la API falla
    with pytest.raises(Exception, match="API Error"):
        translate_text(input_text)
