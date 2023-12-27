import requests
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def inventory (request):
    return HttpResponse("This is inventory home page")