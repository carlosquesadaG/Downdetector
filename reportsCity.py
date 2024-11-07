import requests

# Asignando el token de autenticación proporcionado
API_TOKEN = "eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg"

# Función para obtener el company_id de una compañía
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

# Función para obtener las ciudades con reportes de problemas
def get_cities_with_reports(company_slug, company_id, country_id=136):
    url = f"https://downdetectorapi.com/v2/slugs/{company_slug}/cities?countries={country_id}&companies={company_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code} when fetching cities: {response.text}")
    return None

# Empresas que queremos consultar
companies = ["claro", "movistar", "tigo"]

# Obtener información para cada empresa
for company in companies:
    print(f"Buscando company_id para {company.capitalize()}...")
    company_id = get_company_id(company)
    if company_id:
        print(f"Obteniendo reportes para {company.capitalize()}...")
        # Obtener las ciudades donde hay reportes para la compañía
        cities = get_cities_with_reports(company, company_id)
        if cities:
            print(f"Ciudades con reportes para {company.capitalize()}:")
            for city in cities:
                print(f"Ciudad: {city['city']['name']}, Reportes: {city['amount']}")
        else:
            print(f"No se encontraron reportes para {company.capitalize()}.")
    else:
        print(f"No se encontró el company_id para {company.capitalize()}.")
