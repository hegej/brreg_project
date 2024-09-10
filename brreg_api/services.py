import requests

BASE_URL = 'https://data.brreg.no/enhetsregisteret/api/enheter'

def fetch_companies(page=0, size=100, kommunenummer=None, postnummer=None, org_form=None):
    params = {
        "size": size,
        "page": page,
    }
    if kommunenummer:
        params["kommunenummer"] = kommunenummer
    if postnummer:
        params["postadresse.postnummer"] = postnummer
    if org_form:
        params["organisasjonsform"] = org_form
    
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def get_kommuner():
    url = "https://data.brreg.no/enhetsregisteret/api/kommuner"
    all_kommuner = []
    page = 0
    while True:
        response = requests.get(url, params={"page": page, "size": 100})
        response.raise_for_status()
        data = response.json()
        kommuner = data['_embedded']['kommuner']
        all_kommuner.extend([kommune['nummer'] for kommune in kommuner])
        
        if 'next' not in data['_links']:
            break
        
        page += 1

    return all_kommuner

def get_postnummer_for_kommune(kommunenummer):
    params = {
        "kommunenummer": kommunenummer,
        "size": 10000,
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    postnumre = set()
    for enhet in data.get('_embedded', {}).get('enheter', []):
        if 'postadresse' in enhet and 'postnummer' in enhet['postadresse']:
            postnumre.add(enhet['postadresse']['postnummer'])
    return list(postnumre)

def get_org_forms():
    response = requests.get('https://data.brreg.no/enhetsregisteret/api/organisasjonsformer')
    response.raise_for_status()
    return [form['kode'] for form in response.json()['_embedded']['organisasjonsformer']]

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
        })
    return companies