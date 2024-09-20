python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

---
Construir y levantar los contenedores

docker-compose up --build

Verificar el estado
docker-compose logs -f

Acceso a los servicios:

Puedes acceder al servicio de traducción en http://localhost:5001.
El servicio de almacenamiento en http://localhost:5002.
El servicio de notificaciones en http://localhost:5003.
