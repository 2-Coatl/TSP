# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Define environment variable
ENV NAME StorageService

# Comando para iniciar el servicio
CMD ["python", "main.py"]
