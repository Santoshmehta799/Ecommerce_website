import requests
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def inventory (request):
    return HttpResponse("This is inventory home page")

def add_inventory(request):
    return render(request, 'app_inventory/inventory_add.html')