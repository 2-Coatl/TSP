# Usar una imagen base de Python
FROM python:3.11-slim

# Instalar las dependencias necesarias para PostgreSQL y el cliente
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client \
    curl

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Define environment variable
ENV NAME StorageService
# Dockerfile para las pruebas incluya el directorio del proyecto en PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Comando para iniciar el servicio
CMD ["python", "main.py"]
