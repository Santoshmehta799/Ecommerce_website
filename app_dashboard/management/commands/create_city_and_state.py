import json
import time
from django.core.management.base import BaseCommand
# from app_package.models import Packages, Features
from django.conf import settings

from app_dashboard.models import Cities, States



class Command(BaseCommand):
    help = 'Create default state and city from JSON file'

    def handle(self, *args, **kwargs):
        while True:
            try:
                json_file_path = f'{settings.BASE_DIR}/app_dashboard/static/app_dashboard/state-city.json'
                with open(json_file_path, 'r') as json_file:
                    data = json.load(json_file)

                    # Iterate through all states in the JSON file
                    for state_name, cities in data.items():
                        # Save or update the state in the database
                        state, created = States.objects.get_or_create(name=state_name.upper())

                        # Save or update cities associated with the state
                        for city_name in cities:
                            city, created = Cities.objects.get_or_create(state=state, name=city_name.upper())

                    self.stdout.write(self.style.SUCCESS('Successfully created default state and city .'))

            except FileNotFoundError:
                self.stdout.write(self.style.ERROR("Cant't read json file with name 'state-city.json'."))
                # print("Cant't read json file with name 'feature-ticker.json'.")
                time.sleep(1)
                continue
            break
