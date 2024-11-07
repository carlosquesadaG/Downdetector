import requests

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

# Función para obtener tweets de la compañía usando el company_id
def get_company_tweets(company_id, start_date, end_date, page_size=25):
    url = f"https://downdetectorapi.com/v2/companies/{company_id}/tweets"
    querystring = {
        "startdate": start_date,
        "enddate": end_date,
        "page_size": str(page_size),
        "term": "website",  # Ajusta este parámetro de búsqueda según tus necesidades
        "retweets": "true"
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(url, headers=headers, params=querystring, verify=False)
    if response.status_code == 200:
        tweets = response.json()
        if tweets:
            print(f"Tweets encontrados para company_id {company_id}:")
            for tweet in tweets.get('data', []):
                print(tweet)
        else:
            print(f"No se encontraron tweets para company_id {company_id}.")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Ejecución de las funciones para un ejemplo
company_name = "Claro"
start_date = "2024-11-01T00:00:00+00:00" 
end_date = "2024-11-07T00:00:00+00:00"

# Obtener el company_id
company_id = get_company_id(company_name)

# Si se encuentra el company_id, obtenemos los tweets
if company_id:
    get_company_tweets(company_id, start_date, end_date)
