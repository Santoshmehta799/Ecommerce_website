from django.urls import path
from app_dashboard import views


app_name="app_dashboard"

urlpatterns = [
    path('', views.dashboard_page, name="dashboard-page"),
]
