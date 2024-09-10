import requests
import datetime

BASE_URL = 'https://data.brreg.no/enhetsregisteret/api/enheter'

def fetch_companies(page=0, size=1000, org_form=None, is_bankrupt=None):
    params = {
        "size": size,
        "page": page,
    }
    if org_form:
        params["organisasjonsform"] = org_form
    if is_bankrupt is not None:
        params["konkurs"] = str(is_bankrupt).lower()

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def process_company_data(data):
    companies = []
    for company in data.get('_embedded', {}).get('enheter', []):
        org_form = company.get('organisasjonsform', {}).get('kode', '')
        companies.append({
            'org_number': company['organisasjonsnummer'],
            'name': company['navn'],
            'org_form': org_form,
            'is_bankrupt': company.get('konkurs', False),
            'is_as': org_form == 'AS',
            'postadresse': company.get('postadresse', {}),
            'forretningsadresse': company.get('forretningsadresse', {}),
            'naeringskode1': company.get('naeringskode1', {}),
            'ansatte': company.get('antallAnsatte'),
            'stiftelsesdato': company.get('stiftelsesdato'),
            'registreringsdatoEnhetsregisteret': company.get('registreringsdatoEnhetsregisteret'),
            'registrertIMvaregisteret': company.get('registrertIMvaregisteret', False),
            'frivilligMvaRegistrertBeskrivelser': company.get('frivilligMvaRegistrertBeskrivelser', []),
            'updated_time': datetime.datetime.now(),
        })
    return companies