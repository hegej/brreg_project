from django.core.management.base import BaseCommand
from brreg_api.models import Company
from brreg_api.services import fetch_companies, process_company_data

class Command(BaseCommand):
    help = 'Fetch companies from Brønnøysundregistrene API'

    def handle(self, *args, **options):
        page = 0
        while True:
            self.stdout.write(f"Fetching page {page + 1}...")
            data = fetch_companies(page)
            companies = process_company_data(data)

            if not companies:
                break

            for company_data in dompanies:
                Company.objects.update_or_create(
                    org_number=company_data['org_number'],
                    defaults=company_data
                )

                self.stdout.write(f"Processed {len(companies)} companies")
                page += 1

                self.stdout.write(self.style.SUCCESS('Successfullt fetched and stored company data'))