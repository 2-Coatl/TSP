from abc import ABC, abstractmethod

class ITranslator(ABC):
    """Interfaz para un traductor."""
    
    @abstractmethod
    def translate(self, text: str) -> str:
        """Método abstracto que todas las implementaciones deben sobrescribir.
        
        Args:
            text (str): El texto que se va a traducir.
        
        Returns:
            str: El texto traducido.
        """
        pass
