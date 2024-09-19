from functools import wraps

def handle_error(func):
    """Decorador para manejar errores de manera uniforme"""
    
    @wraps(func)  # Usamos @wraps para mantener el nombre, docstring y metadata de la función decorada
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_message(f"Error en la función {func.__name__}: {str(e)}", level='error')
            raise e
    return wrapper
