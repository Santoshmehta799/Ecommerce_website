from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

import json
import time
from django.core.management.base import BaseCommand
# from app_package.models import Packages, Features
from django.conf import settings


def index_page(request):
    return render(request, 'seventh-square/index.html')


def dashboard_home(request):
    return HttpResponse('this is home page for dashboard')


