import requests

BASE_URL = 'https://data.brreg.no/enhetsregisteret/api/enheter'

def fetch_companies(page=0, size=100):
    params = {
        "size": size,
        "page": page,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def process_company_data(data):
    companies = []
    for company in data.get('_embedded', {}).get('enheter', []):
        companies.append({
            'org_number': company['organisasjonsnummer'],
            'name': company['navn'],
            'is_bankrupt': company.get('konkurs', False),
            'is_as': org_form == 'AS'
        })
    return companies