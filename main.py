import requests
import json

# Definición de ASNs por operador
# asns_colombia = [7161, 27831, 6147, 22927, 27947, 52248]
asns_colombia = [52248]
# Lista de todos los ASNs que quieres consultar

# Parámetros de consulta y encabezados
querystring = {
    "startdate": "2024-11-01T13:37:42+00:00",
    "enddate": "2024-11-06T13:37:42+00:00",
    "interval": "60m",
    "offset": "7m"
}

headers = {
    'authorization': 'Bearer eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg'
}

# URL base de Downdetector para cada ASN
url_template = "https://downdetectorapi.com/v2/networks/{asn}/reports"

# Consulta para cada ASN
for asn in asns_colombia:
    url = url_template.format(asn=asn)
    response = requests.get(url, headers=headers, params=querystring)

    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        try:
            data = response.json()  # Convierte la respuesta a JSON
            print(f"Resultados para ASN {asn}:")
            print(json.dumps(data, indent=4))  # Imprime de forma legible
        except ValueError:
            print(f"Error: La respuesta para ASN {asn} no es un JSON válido.")
    else:
        print(f"No se pudo obtener información para ASN {asn}. Código de estado: {response.status_code}")
