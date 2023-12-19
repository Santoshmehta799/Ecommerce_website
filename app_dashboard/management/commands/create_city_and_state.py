import json
import time
from django.core.management.base import BaseCommand
# from app_package.models import Packages, Features
from django.conf import settings

from app_dashboard.models import Cities, States
import requests
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Fetches state and city data from an API and saves it to the database'

    def populate_states_cities_pincode(self):
        # Clear existing data
        # States.objects.all().delete()
        # Cities.objects.all().delete()

        # Fetch states from the API
        states_api_url = "https://countriesnow.space/api/v0.1/countries/states"
        response_states = requests.post(states_api_url, json={"country": "india"})

        if response_states.status_code == 200:
            india_data_states = response_states.json()['data']['states']

            for state_data in india_data_states:
                try:
                    state_name = state_data['name']
                    state_code = state_data['state_code']

                    # Save the state to the database
                    state, created = States.objects.get_or_create(name=state_name.upper(), defaults={"state_code":state_code})
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"State '{state_name}' created."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"State '{state_name}' already exists."))

                    # Fetch and save cities for each state
                    print("=====================>",state_name)
                    cities_api_url = "https://countriesnow.space/api/v0.1/countries/state/cities"
                    response_cities = requests.post(cities_api_url, json={"country": "india", "state": state_name})

                    if response_cities.status_code == 200:
                        india_data_cities = response_cities.json()['data']
                        print("=================>",india_data_cities)
                        for city_name in india_data_cities:
                            try:
                                # Try to create the city; if it already exists, catch the IntegrityError
                                city, city_created = Cities.objects.get_or_create(state=state, name=city_name.upper())
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

        else:
            self.stdout.write(self.style.ERROR(f"Error fetching Indian states. "
                                               f"Status code: {response_states.status_code}, "
                                               f"Response content: {response_states.text}"))

        self.stdout.write(self.style.SUCCESS("Data populated successfully!"))

    def handle(self, *args, **options):
        self.populate_states_cities_pincode()




