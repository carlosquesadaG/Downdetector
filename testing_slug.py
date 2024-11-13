import requests
import json

companyId = 136
countryId = 136
Slugs = 'facebook'
bearer = 'eyJhbGciOiJIUzUxMiIsImtpZCI6Ino2eHdrenAyZTMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkiLCJpYXQiOjE3MzA5MjQzOTksImp0aSI6ImI5NjYwYTI5LWI1MWUtNDNlOC1iNWM3LTRjODMyYTEzZTNlZiJ9.iE_gtLlilo3jhaCRif6E42cMtq29TZ4jE6VSN3fVidM1POCDegG4Q6H6Dt93BfyFRxU3nrhbB7QWcqhG_MigYg'

def get_company_id(company_name):
    url = f"https://downdetectorapi.com/v2/companies/search?fields=id,name,slug,country_iso,indicators,site_id&name={company_name}"
    headers = {
        "Authorization": f"Bearer {bearer}"
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


url = "https://downdetectorapi.com/v2/slugs/{Slugs}/reportscountries=${countryId}&companies=${companyId}"

querystring = {
    "startdate": "2024-11-06T00:00:00+00:00",
    "enddate": "2024-11-07T00:00:00+00:00"
}

headers = {
    'authorization': 'Bearer {bearer}'
}

response = requests.get(url, headers=headers, params=querystring, verify=False)

print(response.text)
