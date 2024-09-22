#!/bin/bash
set -e

echo "Iniciando la inicialización de la base de datos..."

# Usar variables de entorno con valores por defecto
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"
POSTGRES_DB="${POSTGRES_DB:-postgres}"
DB_USER="${DB_USER:-pdf_translator}"
DB_PASSWORD="${DB_PASSWORD:-secure_password}"
DB_NAME="${DB_NAME:-pdf_translation_db}"

echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_DB: $POSTGRES_DB"
echo "DB_USER: $DB_USER"
echo "DB_NAME: $DB_NAME"

# Función para ejecutar comandos SQL
psql_command() {
    PGPASSWORD="$POSTGRES_PASSWORD" psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$1" -c "$2"
}

echo "Creando usuario $DB_USER si no existe..."
psql_command "$POSTGRES_DB" "DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
        RAISE NOTICE 'Usuario \"$DB_USER\" creado.';
    ELSE
        RAISE NOTICE 'Usuario \"$DB_USER\" ya existe. Omisión de creación.';
    END IF;
END
\$\$;"

echo "Creando base de datos $DB_NAME si no existe..."
psql_command "$POSTGRES_DB" "SELECT 'CREATE DATABASE $DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME');"
psql_command "$POSTGRES_DB" "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo "La base de datos $DB_NAME ya existe."

echo "Otorgando privilegios al usuario $DB_USER en la base de datos $DB_NAME..."
psql_command "$POSTGRES_DB" "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "Conectando a la base de datos $DB_NAME para otorgar privilegios en el esquema public..."
psql_command "$DB_NAME" "GRANT ALL ON SCHEMA public TO $DB_USER;"

echo "La inicialización de la base de datos se ha completado."