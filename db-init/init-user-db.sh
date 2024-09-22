#!/bin/bash
: '
Asegúrate de que el script init-user-db.sh tiene permisos de ejecución. 
chmod +x ./db-init/init-user-db.sh
'
set -e

echo "Iniciando la inicialización de la base de datos..."
echo "Iniciando la inicialización de la base de datos..."
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_DB: $POSTGRES_DB"
echo "DB_USER: $DB_USER"
echo "DB_NAME: $DB_NAME"


# Usar variables de entorno
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_DB=${POSTGRES_DB:}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=${DB_NAME}

# Función para ejecutar comandos SQL con autenticación
function run_sql() {
    PGPASSWORD=$POSTGRES_PASSWORD psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$1" -c "$2"
}

echo "Creando usuario $DB_USER si no existe..."
run_sql "$POSTGRES_DB" "DO \$\$
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
run_sql "$POSTGRES_DB" "SELECT 'CREATE DATABASE $DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec"

echo "Otorgando privilegios al usuario $DB_USER en la base de datos $DB_NAME..."
run_sql "$POSTGRES_DB" "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "Conectando a la base de datos $DB_NAME para otorgar privilegios en el esquema public..."
run_sql "$DB_NAME" "GRANT ALL ON SCHEMA public TO $DB_USER;"

echo "La inicialización de la base de datos se ha completado."