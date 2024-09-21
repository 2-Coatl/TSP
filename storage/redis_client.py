import redis
import os
from utils.decorators import handle_error
from utils.logger import LoggerManager

class RedisClient:
    def __init__(self):
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.client = redis.from_url(redis_url)
        LoggerManager.log_message(f"Redis client initialized with URL: {redis_url}", level='info')

    @handle_error
    def publish(self, channel, message):
        """
        Publica un mensaje en un canal específico.
        
        :param channel: El canal en el que publicar
        :param message: El mensaje a publicar
        :return: El número de clientes que recibieron el mensaje
        """
        result = self.client.publish(channel, message)
        LoggerManager.log_message(f"Message published to channel '{channel}': {message}", level='info')
        return result

    @handle_error
    def subscribe(self, channel):
        """
        Suscribe al cliente a un canal específico.
        
        :param channel: El canal al que suscribirse
        :return: Un objeto PubSub para escuchar mensajes
        """
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        LoggerManager.log_message(f"Subscribed to channel: {channel}", level='info')
        return pubsub

    @handle_error
    def get(self, key):
        """
        Obtiene el valor asociado a una clave.
        
        :param key: La clave a buscar
        :return: El valor asociado a la clave, o None si no existe
        """
        value = self.client.get(key)
        if value:
            LoggerManager.log_message(f"Retrieved value for key: {key}", level='info')
        else:
            LoggerManager.log_message(f"No value found for key: {key}", level='warning')
        return value

    @handle_error
    def set(self, key, value, expiration=None):
        """
        Establece un valor para una clave, con una expiración opcional.
        
        :param key: La clave a establecer
        :param value: El valor a asociar con la clave
        :param expiration: Tiempo de expiración en segundos (opcional)
        :return: True si se estableció correctamente, False en caso contrario
        """
        result = self.client.set(key, value, ex=expiration)
        if result:
            LoggerManager.log_message(f"Set value for key: {key}, expiration: {expiration}", level='info')
        else:
            LoggerManager.log_message(f"Failed to set value for key: {key}", level='error')
        return result

    @handle_error
    def delete(self, key):
        """
        Elimina una clave y su valor asociado.
        
        :param key: La clave a eliminar
        :return: El número de claves eliminadas (0 o 1)
        """
        result = self.client.delete(key)
        if result:
            LoggerManager.log_message(f"Deleted key: {key}", level='info')
        else:
            LoggerManager.log_message(f"Key not found for deletion: {key}", level='warning')
        return result

    @handle_error
    def close(self):
        """
        Cierra la conexión con Redis.
        """
        self.client.close()
        LoggerManager.log_message("Redis connection closed", level='info')