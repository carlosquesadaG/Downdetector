import requests

# Asignando el token de autenticación proporcionado
API_TOKEN = "eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg"

# Función para obtener el company_id de una compañía
def get_company_id(company_name):
    url = f"https://downdetectorapi.com/v2/companies/search?fields=id,name,slug,country_iso,indicators,site_id&name={company_name}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        companies = response.json()
        # Filtramos la compañía de Colombia (código de país "CO" es 136)
        if companies:
            for company in companies:
                if company.get('country_iso') == 'CO':
                    print(f"Company found: {company['name']} with ID: {company['id']}")
                    return company['id']
        else:
            print(f"No companies found for name: {company_name}")
    else:
        print(f"Error {response.status_code}: {response.text}")
    return None

# Función para obtener los tweets de una compañía utilizando el company_id
def get_company_tweets(company_id, start_date, end_date, page_size=25):
    url = f"https://downdetectorapi.com/v2/companies/{company_id}/tweets"
    querystring = {
        "startdate": start_date,
        "enddate": end_date,
        "page_size": str(page_size),
        "retweets": "true",  # Considerar los retweets
        "term": "website",  # Ejemplo de búsqueda por término
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
    return None

# Empresas que queremos consultar
companies = ["claro", "movistar", "tigo"]

# Fechas de inicio y fin para la consulta (puedes modificarlas según tu necesidad)
start_date = "2024-11-06T00:00:00+00:00"
end_date = "2024-11-07T00:00:00+00:00"

# Obtener tweets para cada empresa
for company in companies:
    print(f"Buscando company_id para {company.capitalize()}...")
    company_id = get_company_id(company)
    if company_id:
        print(f"Obteniendo tweets para {company.capitalize()}...")
        # Obtener los tweets de la compañía
        tweets = get_company_tweets(company_id, start_date, end_date)
        if tweets:
            print(f"Tweets para {company.capitalize()}:")
            for tweet in tweets:
                print(f"Tweet: {tweet['text']}")
        else:
            print(f"No se encontraron tweets para {company.capitalize()}.")
    else:
        print(f"No se encontró el company_id para {company.capitalize()}.")
