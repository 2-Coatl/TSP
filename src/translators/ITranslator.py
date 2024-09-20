class Translator:
    """Interfaz para un traductor."""
    
    def translate(self, text: str) -> str:
        """Método abstracto que todas las implementaciones deben sobreescribir.
        
        Args:
            text (str): El texto que se va a traducir.
        
        Returns:
            str: El texto traducido.
        """
        raise NotImplementedError("Esta es una interfaz. Las subclases deben implementar el método translate.")
