from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from app_user import forms as user_forms, methods as user_methods


def index_page(request):
    success = ""
    error = ""
    
    if request.user.is_authenticated:
        return redirect('app_dashboard:dashboard-page')
    
    form = user_forms.auth.RegisterForm()
    context = {
        'error' : error,
        'success' : success,
        'form' :form,
    }
    return render(request, 'seventh-square/index.html', context)

@login_required
def dashboard_page(request):
    return render(request, 'app_dashboard/dashboard.html')


