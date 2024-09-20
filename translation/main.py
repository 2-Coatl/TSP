import requests

storage_service_url = "http://storage_service:5000/get_file"
response = requests.get(storage_service_url, params={"file_id": "12345"})

if response.status_code == 200:
    file_content = response.json().get("content")
    # Realizar operaciones de traducción aquí
