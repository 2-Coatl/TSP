#!/bin/bash

: '
Este script se utiliza para cambiar la contraseña de un usuario en PostgreSQL.
Haz el script ejecutable:  
chmod +x change_user_password.sh

Ejecuta el script: Proporciona el nombre de usuario y la nueva contraseña como argumentos. 
Por ejemplo: 
./change_user_password.sh postgres nueva_contraseña
./change_user_password.sh postgres tspadmin123
'


# Comprobar si se proporcionaron argumentos
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <nombre_usuario> <nueva_contraseña>"
    exit 1
fi

# Variables
DB_USER="$1" # Nombre de usuario pasado como argumento
NEW_PASSWORD="$2" # Contraseña pasada como argumento

# Verificar si el usuario existe en PostgreSQL
if sudo -u postgres psql -t -c "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER';" | grep -q 1; then
    # Cambiar la contraseña si el usuario existe
    if sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$NEW_PASSWORD';"; then
        echo "La contraseña de '$DB_USER' se ha actualizado correctamente."
    else
        # Mensaje de error si no se pudo actualizar la contraseña
        echo "Error: No se pudo actualizar la contraseña de '$DB_USER'."
    fi
else
    # Mensaje si el usuario no existe
    echo "El usuario '$DB_USER' no existe."
fi
