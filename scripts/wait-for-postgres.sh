#!/bin/sh
# wait-for-postgres.sh

set -e

# Parámetros por defecto
POSTGRES_HOST=${POSTGRES_HOST}
POSTGRES_USER=${POSTGRES_USER:-"$DB_USER"}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-"$DB_PASSWORD"}
POSTGRES_DB=${POSTGRES_DB:-"$DB_NAME"}
TIMEOUT=${TIMEOUT}
INTERVAL=${INTERVAL}

# Función de uso
usage() {
    echo "Usage: $0 [-h <host>] [-U <user>] [-P <password>] [-d <database>] [-t <timeout>] [-i <interval>] [-- <command>...]"
    exit 1
}

# Procesar opciones de línea de comandos
while getopts "h:U:P:d:t:i:" opt; do
    case $opt in
        h) POSTGRES_HOST=$OPTARG ;;
        U) POSTGRES_USER=$OPTARG ;;
        P) POSTGRES_PASSWORD=$OPTARG ;;
        d) POSTGRES_DB=$OPTARG ;;
        t) TIMEOUT=$OPTARG ;;
        i) INTERVAL=$OPTARG ;;
        *) usage ;;
    esac
done

shift $((OPTIND - 1))
cmd="$@"

# Función para intentar la conexión
try_connect() {
    PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' > /dev/null 2>&1
}

# Esperar a que PostgreSQL esté disponible
start_time=$(date +%s)
while ! try_connect; do
    elapsed=$(($(date +%s) - start_time))
    if [ $elapsed -ge $TIMEOUT ]; then
        echo >&2 "Error: Timed out waiting for PostgreSQL to become available"
        exit 1
    fi
    echo >&2 "PostgreSQL is unavailable - sleeping"
    sleep $INTERVAL
done

echo >&2 "PostgreSQL is up - executing command"
exec $cmd