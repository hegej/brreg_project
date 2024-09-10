from django.core.management.base import BaseCommand
from brreg_api.models import Company
from brreg_api.services import fetch_companies, process_company_data
import requests
import time

BASE_URL = 'https://data.brreg.no/enhetsregisteret/api/enheter'

class Command(BaseCommand):
    help = 'Fetch companies from Brønnøysundregistrene API'

    def handle(self, *args, **options):
        valg = input("Velg handling:\n1. Hent konkursbedrifter\n2. Tell antall AS'er\n")

        if valg == '1':
            self.fetch_bankrupt_companies()
        elif valg == '2':
            self.count_as_companies()
        else:
            self.stdout.write(self.style.ERROR('Ugyldig valg'))

    def fetch_bankrupt_companies(self):
        start_time = time.time() 
        while True:
            self.stdout.write(f"Fetching bankrupt companies")
            try:
                data = fetch_companies(size=10000, is_bankrupt=True)
                companies = process_company_data(data)

                if not companies:
                    break

                for company_data in companies:
                    company, created = Company.objects.update_or_create(
                        org_number=company_data['org_number'],
                        defaults=company_data
                    )

                self.stdout.write(f" Processed {len(companies)} companies")

                if 'next' not in data.get('_links', {}):
                    break

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 400:
                    self.write_message("Reached the end of data", self.style.WARNING)
                    break
                else:
                    self.write_message(f"HTTP error occurred: {e}", self.style.ERROR)
            except Exception as e:
                self.write_message(f"An error occurred: {e}", self.style.ERROR)

        end_time = time.time()
        elapsed_time = end_time - start_time

        bankrupt_companies_count = Company.objects.filter(is_bankrupt=True).count()
        self.stdout.write(self.style.SUCCESS(f'Successfully fetched and stored {bankrupt_companies_count} bankrupt companies'))
        self.stdout.write(self.style.SUCCESS(f'Query completed in {elapsed_time:.2f} seconds')) 

    def count_as_companies(self):
        start_time = time.time()
        response = requests.get(BASE_URL, params={"organisasjonsform": "AS"})
        response.raise_for_status()
        data = response.json()
        total_as_companies = data['page']['totalElements']

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.write_message(f'Number of AS companies: {total_as_companies}', self.style.SUCCESS)
        self.stdout.write(self.style.SUCCESS(f'Query completed in {elapsed_time:.2f} seconds'))

    def write_message(self, message, style=None):
        if style:
            self.stdout.write(style(message))
        else:
            self.stdout.write(message)