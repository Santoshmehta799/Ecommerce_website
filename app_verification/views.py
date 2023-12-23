from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.


def verification_home(request):
    return HttpResponse("hello , testing!")

def get_detail(request):
    return render(request, 'app_verification/gst_detail.html')

def general_detail(request):
    return render(request, 'app_verification/general_detail.html')

    

