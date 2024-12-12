# Proyecto TSP

## Requisitos previos

Asegúrate de tener instalados los siguientes componentes:

1. PostgreSQL y postgresql-contrib
2. Docker 
3. Docker Compose

## Instalación

### 1. PostgreSQL

Para instalar PostgreSQL y postgresql-contrib, ejecuta:

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib -y
```

### 2. Docker y Docker Compose

Sigue las [instrucciones oficiales de Docker](https://docs.docker.com/engine/install/ubuntu/) para instalar Docker en Ubuntu.

Para instalar Docker Compose, sigue las [instrucciones oficiales de Docker Compose](https://docs.docker.com/compose/install/).

## Configuración

Asegúrate de que los siguientes archivos tengan los permisos correctos (755):

```bash
chmod 755 db-init/init-user-db.sh
chmod 755 scripts/change_user_password.sh
chmod 755 scripts/wait-for-postgres.sh
```

Después de asignar los permisos, puedes cambiar la contraseña del usuario de PostgreSQL ejecutando el script `change_user_password.sh`. Por ejemplo:

```bash
bash scripts/change_user_password.sh postgres nueva_contraseña
```

Asegúrate de reemplazar `nueva_contraseña` con la contraseña que deseas establecer.

## Ejecución del proyecto

### Iniciar los contenedores

Puedes usar cualquiera de los siguientes comandos para iniciar los contenedores:

Para construir las imágenes (usando caché si está disponible) e iniciar los contenedores en un solo comando:
```bash
docker compose up --build
```

Para construir las imágenes sin usar caché y luego iniciar los contenedores:

```bash
docker compose build --no-cache
docker compose up
```

o para ejecutar en modo detached:

```bash
docker compose up -d
```

### Detener los contenedores

Si algo sale mal y necesitas detener los contenedores, puedes usar:

```bash
docker compose down -v
```

Este comando detendrá y eliminará los contenedores y volúmenes.

Si solo quieres detener los contenedores sin eliminar los volúmenes:

```bash
docker compose down
```

## Pruebas

Para reconstruir la imagen de prueba y ejecutar las pruebas:

```bash
docker compose build test
docker compose run --rm test
```


## Acceso a los servicios:

Puedes acceder al servicio de traducción en http://localhost:5001.
El servicio de almacenamiento en http://localhost:5002.
El servicio de notificaciones en http://localhost:5003.
