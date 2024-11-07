import requests

# Token de API de Downdetector
API_TOKEN = 'eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg'


#company_id
def get_company_id(company_name):
    url = f"https://downdetectorapi.com/v2/companies/search?fields=id,name,slug,country_iso,indicators,site_id&name={company_name}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        companies = response.json()
        #para col es el 136
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

# Función para obtener términos de tweets de una compañía usando el company_id
def get_company_tweet_terms(company_id, start_date, end_date, filter_terms="internet,connection", exclude_terms="comcast,my-term,.*my.regexp.*", amount=25):
    url = f"https://downdetectorapi.com/v2/companies/{company_id}/tweets/terms"
    querystring = {
        "startdate": start_date,
        "enddate": end_date,
        "filter": filter_terms,
        "exclude": exclude_terms,
        "amount": str(amount)
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(url, headers=headers, params=querystring, verify=False)
    if response.status_code == 200:
        tweet_terms = response.json()
        if tweet_terms:
            print(f"Términos de tweets encontrados para company_id {company_id}:")
            for term in tweet_terms.get('data', []):
                print(term)
        else:
            print(f"No se encontraron términos de tweets para company_id {company_id}.")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Ejecución de las funciones para un ejemplo
company_name = "Claro"
start_date = "2024-11-01T00:00:00+00:00"  # Ajusta las fechas a tu preferencia
end_date = "2024-11-06T23:59:59+00:00"    # Ajusta las fechas a tu preferencia

# Obtener el company_id
company_id = get_company_id(company_name)

# Si se encuentra el company_id, obtenemos los términos de tweets
if company_id:
    get_company_tweet_terms(company_id, start_date, end_date)
