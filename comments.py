import requests

# Token de API de Downdetector
API_TOKEN = 'eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg'

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


# Función para obtener comentarios de una compañía usando el company_id
def get_company_comments(company_id, start_date, end_date, filter_terms="internet,connection", exclude_terms="comcast,my-term,.*my.regexp.*", amount=25):
    url = f"https://downdetectorapi.com/v2/companies/{company_id}/comments/terms"
    querystring = {
        "startdate": start_date,
        "enddate": end_date,
        "filter": filter_terms,  # Filtros de términos específicos
        "exclude": exclude_terms,  # Términos a excluir
        "amount": str(amount)  # Cantidad de comentarios
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(url, headers=headers, params=querystring, verify=False)
    if response.status_code == 200:
        comments = response.json()
        if comments:
            print(f"Comentarios encontrados para company_id {company_id}:")
            for comment in comments.get('data', []):
                print(comment)
        else:
            print(f"No se encontraron comentarios para company_id {company_id}.")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Ejecución de las funciones para un ejemplo
company_name = "movistar"
start_date = "2024-11-06T00:00:00+00:00"  # Ajusta las fechas a tu preferencia
end_date = "2024-11-07T00:59:59+00:00"    # Ajusta las fechas a tu preferencia

# Obtener el company_id
company_id = get_company_id(company_name)

# Si se encuentra el company_id, obtenemos los comentarios
if company_id:
    get_company_comments(company_id, start_date, end_date)
