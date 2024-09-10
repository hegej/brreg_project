from django.core.management.base import BaseCommand
from brreg_api.models import Company
from brreg_api.services import fetch_companies, process_company_data, get_kommuner, get_postnummer_for_kommune, get_org_forms
import requests

class Command(BaseCommand):
    help = 'Fetch companies from Brønnøysundregistrene API'

    def handle(self, *args, **options):
        total_companies = 0
        bankrupt_companies = 0
        as_companies = 0

        kommuner = get_kommuner()
        org_forms = get_org_forms()
        self.stdout.write(f"Found {len(kommuner)} kommuner and {len(org_forms)} organisasjonsformer")

        for i, kommune in enumerate(kommuner, 1):
            postnumre = get_postnummer_for_kommune(kommune)
            self.stdout.write(f"Processing kommune {i}/{len(kommuner)}: {kommune} - Found {len(postnumre)} postnumre")

            for j, postnummer in enumerate(postnumre, 1):
                self.stdout.write(f"  Processing postnummer {j}/{len(postnumre)}: {postnummer}")
                for k, org_form in enumerate(org_forms, 1):
                    page = 0
                    while True:
                        self.stdout.write(f"    Fetching companies for org_form {k}/{len(org_forms)}: {org_form}, page {page + 1}")
                        try:
                            data = fetch_companies(page, size=100, kommunenummer=kommune, postnummer=postnummer, org_form=org_form)
                            companies = process_company_data(data)
                            
                            if not companies:
                                break

                            for company_data in companies:
                                company, created = Company.objects.update_or_create(
                                    org_number=company_data['org_number'],
                                    defaults=company_data
                                )
                                if company.is_as:
                                    as_companies += 1
                                if company.is_bankrupt:
                                    bankrupt_companies += 1
                                total_companies += 1

                            self.stdout.write(f"      Processed {len(companies)} companies")
                            
                            if 'next' not in data.get('_links', {}):
                                break
                            
                            page += 1

                        except requests.exceptions.HTTPError as e:
                            if e.response.status_code == 400:
                                self.stdout.write(self.style.WARNING(f"      Reached the end of data for this combination"))
                                break
                            else:
                                self.stdout.write(self.style.ERROR(f"      HTTP error occurred: {e}"))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"      An error occurred: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Finished processing kommune {kommune}"))
            self.stdout.write(f"Current totals: {total_companies} companies, {as_companies} AS, {bankrupt_companies} bankrupt")

        self.stdout.write(self.style.SUCCESS(f'Successfully fetched and stored {total_companies} companies in total'))
        self.stdout.write(self.style.SUCCESS(f'Number of AS companies: {as_companies}'))
        self.stdout.write(self.style.SUCCESS(f'Number of bankrupt companies: {bankrupt_companies}'))