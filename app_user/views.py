from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.


def auth_home(request):
    return HttpResponse("hello , testing!")

    
