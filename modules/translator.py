import openai

openai.api_key = 'TU_API_KEY'

def translate_text(text):
    """Traduce el texto usando la API de GPT."""
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=f"Traduce el siguiente texto al español latino:\n\n{text}",
            max_tokens=2000
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error durante la traducción: {str(e)}")
