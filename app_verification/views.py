from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.


def verification_home(request):
    return HttpResponse("hello , testing!")

    

