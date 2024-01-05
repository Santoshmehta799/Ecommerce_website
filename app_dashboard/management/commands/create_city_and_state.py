import json
import time
from django.core.management.base import BaseCommand
# from app_package.models import Packages, Features
from django.conf import settings

from app_dashboard.models import Cities, Country, States
import requests
from django.db import IntegrityError

# python manage.py create_city_and_state
class Command(BaseCommand):
    help = 'Fetches state and city data from an API and saves it to the database'

    def populate_states_cities(self):
        # Clear existing data
        # States.objects.all().delete()
        # Cities.objects.all().delete()

        # Fetch states from the API
        country_api_url = "https://countriesnow.space/api/v0.1/countries/states"
        response_country = requests.get(country_api_url)
        country_data = response_country.json()['data']
        for country in country_data:
            country_name = country['name']
            country_iso2_code = country['iso2']
            country_iso3_code = country['iso3']
            states_list = country['states']

            try:
                country_obj, created = Country.objects.get_or_create(name=country_name,
                    defaults={"iso2_code": country_iso2_code,"iso3_code": country_iso3_code})
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Country '{country_name}' created."))
            except IntegrityError:
                # Country already exists; handle this case as needed
                self.stdout.write(self.style.SUCCESS(f"Country '{country_name}' already exists. Skipping..."))
                continue

            for state_data in states_list:
                try:
                    state_name = state_data['name']
                    state_code = state_data['state_code']

                    # Save the state to the database
                    state, created = States.objects.get_or_create(name=state_name.upper(),country=country_obj,
                        defaults={"state_code":state_code})
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"State '{state_name}' created."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"State '{state_name}' already exists."))


                    if country_obj.name == 'INDIA': 
                        # Fetch and save cities for each state
                        cities_api_url = "https://countriesnow.space/api/v0.1/countries/state/cities"
                        response_cities = requests.post(cities_api_url, json={"country": f"{country_obj.name.lower()}",
                            "state": state_name})

                        if response_cities.status_code == 200:
                            india_data_cities = response_cities.json()['data']
                            print("=================>",india_data_cities)
                            for city_name in india_data_cities:
                                try:
                                    # Try to create the city; if it already exists, catch the IntegrityError
                                    city, city_created = Cities.objects.get_or_create(state=state, name=city_name)
                                    if city_created:
                                        self.stdout.write(self.style.SUCCESS(f"City '{city_name}' in state '{state_name}' created."))
                                    else:
                                        self.stdout.write(self.style.SUCCESS(f"City '{city_name}' in state '{state_name}' already exists."))
                                except IntegrityError:
                                    self.stdout.write(self.style.SUCCESS(f"City '{city_name}' in state '{state_name}' already exists."))

                        else:
                            self.stdout.write(self.style.ERROR(f"Error fetching cities for state '{state_name}'. "
                                                            f"Status code: {response_cities.status_code}, "
                                                            f"Response content: {response_cities.text}"))
                            
                except IntegrityError:
                    self.stdout.write(self.style.SUCCESS(f"State '{state_name}' (Code: {state_code}) already exists."))

        self.stdout.write(self.style.SUCCESS("Data populated successfully!"))

    def handle(self, *args, **options):
        self.populate_states_cities()




