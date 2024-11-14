import requests
import json
slugs = 'movistar'
url = f"https://downdetectorapi.com/v2/slugs/{slugs}/locations"
bearer = 'eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg'

headers = {'Authorization': f'Bearer {bearer}'}

query = {"page_size":"10"}

response = requests.get(url, headers=headers, verify=False, params=query)

# Verificar si la respuesta es exitosa
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))  # Imprimir JSON formateado
else:
    print(f"{response}")
    print(f"Error: {response.status_code}")
