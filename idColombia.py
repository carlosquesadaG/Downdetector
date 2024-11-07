import requests

# Definir la URL de la API para obtener todos los sitios
url = "https://downdetectorapi.com/v2/sites"

# Definir los headers de la solicitud (incluyendo el token de autorización)
headers = {
    'authorization': 'Bearer eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg'
}

# Realizar la solicitud GET a la API
response = requests.get(url, headers=headers)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    try:
        # Convertir la respuesta a formato JSON
        sites = response.json()
        
        # Buscar el país Colombia (CO)
        colombia_data = next((site for site in sites if site['country']['iso'] == 'CO'), None)
        
        if colombia_data:
            # Mostrar el ID del país y otros detalles de Colombia
            print(f"ID de Colombia: {colombia_data['country_id']}")
            print(f"Nombre del dominio: {colombia_data['name']}")
            print(f"Twitter: {colombia_data['twitter']}")
        else:
            print("No se encontró información sobre Colombia.")
    except ValueError:
        print("Error: La respuesta no es un JSON válido.")
else:
    print(f"Error al obtener los sitios. Código de estado: {response.status_code}")
    print(f"Detalles del error: {response.text}")
