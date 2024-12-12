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

# Copiar todo el contenido del directorio actual
COPY . .

# Set environment variables
ENV NAME StorageService
ENV PYTHONPATH=/app:$PYTHONPATH
ENV PYTHONUNBUFFERED 1

# Cambiar al directorio padre de 'src' y ejecutar como módulo
CMD ["python", "-m", "src.main"]