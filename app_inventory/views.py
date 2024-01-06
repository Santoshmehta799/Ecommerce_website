import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.


def inventory (request):
    return HttpResponse("This is inventory home page")

def add_inventory_step_1(request):
    if request.method == 'POST':
        return redirect('app_inventory:add_inventory_step_2')
    return render(request, 'app_inventory/add_product_step_1.html')

def add_inventory_step_2(request):
    return render(request, 'app_inventory/add_product_step_2.html')

def add_inventory_step_3(request):
    return render(request, 'app_inventory/add_product_step_3.html')

def add_inventory_step_4(request):
    return render(request, 'app_inventory/add_product_step_4.html')

def add_inventory_step_5(request):
    return render(request, 'app_inventory/add_product_step_5.html')

