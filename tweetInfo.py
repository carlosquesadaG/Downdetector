import requests
import json  # Importa el módulo JSON

# Token de API de Downdetector
API_TOKEN = 'eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg'

# Función para obtener el company_id de una compañía
def get_company_id(company_name):
    url = f"https://downdetectorapi.com/v2/companies/search?fields=id,name,slug,country_iso,indicators,site_id&name={company_name}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        companies = response.json()
        if companies:
            for company in companies:
                if company.get('country_iso') == 'CO':  # Solo toma las compañías en Colombia
                    print(f"Company found: {company['name']} with ID: {company['id']}")
                    return company['id']
        else:
            print(f"No companies found for name: {company_name}")
    else:
        print(f"Error {response.status_code}: {response.text}")
    return None

# Función para obtener tweets de la compañía usando el company_id y formatear la salida en JSON
def get_company_tweets(company_id, start_date, end_date, page_size=25):
    url = f"https://downdetectorapi.com/v2/companies/{company_id}/tweets"
    querystring = {
        "startdate": start_date,
        "enddate": end_date,
        "page_size": str(page_size),
        "term": "servicio",
        "retweets": "true"
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(url, headers=headers, params=querystring, verify=False)
    if response.status_code == 200:
        tweets = response.json()
        if isinstance(tweets, dict) and 'data' in tweets:
            # Almacenar los tweets en una lista
            tweet_list = []
            for tweet in tweets['data']:
                tweet_list.append(tweet)
            
            # Imprimir los tweets formateados como JSON
            print(json.dumps({"tweets": tweet_list}, indent=4, ensure_ascii=False))
        else:
            print(json.dumps({"message": f"No se encontraron tweets o la estructura de datos no es la esperada para company_id {company_id}."}, indent=4))
    else:
        print(json.dumps({"error": f"Error {response.status_code}: {response.text}"}, indent=4))

# Ejecución de las funciones para un ejemplo
company_name = "Claro"
start_date = "2024-11-05T00:00:00+00:00" 
end_date = "2024-11-07T00:00:00+00:00"

# Obtener el company_id
company_id = get_company_id(company_name)

# Si se encuentra el company_id, obtenemos los tweets
if company_id:
    get_company_tweets(company_id, start_date, end_date)
