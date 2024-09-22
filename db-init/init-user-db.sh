#!/bin/bash
set -e

echo "Iniciando la inicialización de la base de datos para el Proyecto de Traducción de PDF..."

# Usar variables de entorno o valores predeterminados para la conexión a PostgreSQL
POSTGRES_USER=${POSTGRES_USER:-postgres}
POSTGRES_DB=${POSTGRES_DB:-postgres}

# Usar variables de entorno o valores predeterminados para la aplicación
DB_USER=${DB_USER:-pdf_translator}
DB_PASSWORD=${DB_PASSWORD:-secure_password}
DB_NAME=${DB_NAME:-pdf_translation_db}

# Crear usuario si no existe
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO
    \$do\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN
            CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
            RAISE NOTICE 'Usuario "$DB_USER" creado.';
        ELSE
            RAISE NOTICE 'Usuario "$DB_USER" ya existe. Omisión de creación.';
        END IF;
    END
    \$do\$;
EOSQL

# Crear base de datos si no existe
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    SELECT 'CREATE DATABASE $DB_NAME'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec;
    
    -- Otorgar privilegios al usuario en la base de datos
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
    GRANT ALL ON SCHEMA public TO $DB_USER;
EOSQL

echo "La inicialización de la base de datos para el Proyecto de Traducción de PDF se ha completado."
