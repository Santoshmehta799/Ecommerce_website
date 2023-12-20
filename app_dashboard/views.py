from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def index_page(request):
    if request.user.is_authenticated:
        return redirect('app_dashboard:dashboard-page')
    return render(request, 'seventh-square/index.html')

@login_required
def dashboard_page(request):
    return render(request, 'app_dashboard/dashboard.html')


