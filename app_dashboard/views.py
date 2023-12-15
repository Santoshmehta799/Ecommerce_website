from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

import json
import time
from django.core.management.base import BaseCommand
# from app_package.models import Packages, Features
from django.conf import settings


def dashboard_home(request):
    return HttpResponse('this is home page for dashboard')





class Command(BaseCommand):
    help = 'Create default package from JSON file'

    def handle(self, args, *kwargs):
        while True:
            try:
                json_file_path = f'{settings.BASE_DIR}/app_dashboard/static/app_dashboard/state-city.json'
                with open(json_file_path, 'r') as json_file:
                    data = json.load(json_file)

                    for item in data:
                        print("----------->",item)
                    #     name = item.get('name')
                    #     currency = item.get('currency')
                    #     price = item.get('price')
                    #     period = item.get('period')
                    #     duration = item.get('duration')
                    #     is_active = item.get('is_active')
                    #     features = item.get('features')

                    #     # Create a FutureTickerManager object
                    #     package_obj, created = Packages.objects.get_or_create(currency=currency, name=name,
                    #         defaults={'price': price,'period': period,})
                    #     package_obj.is_active = is_active
                    #     package_obj.price = price
                    #     package_obj.images = None
                    #     package_obj.period = period
                    #     package_obj.duration = duration
                    #     package_obj.save()

                    #     for feature in features:
                    #         key =  feature.get('key')
                    #         char_value =  feature.get('char_value')
                    #         int_value =  feature.get('int_value')
                    #         feature_is_active =  feature.get('is_active')
                    #         feature_obj, created = Features.objects.get_or_create(package=package_obj, key=key)
                    #         feature_obj.char_value = char_value
                    #         feature_obj.int_value = int_value
                    #         feature_obj.is_active = feature_is_active
                    #         feature_obj.save()

                    # self.stdout.write(self.style.SUCCESS('Successfully created packages and features.'))

            except FileNotFoundError:
                self.stdout.write(self.style.ERROR("Cant't read json file with name 'default-package.json'."))
                # print("Cant't read json file with name 'feature-ticker.json'.")
                time.sleep(1)
                continue
            break