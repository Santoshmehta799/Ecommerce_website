from django.urls import path
from app_dashboard import views


app_name="app_dashboard"

urlpatterns = [
    path('', views.dashboard_page, name="dashboard-page"),
    #ajax load
    path('load-city/', views.load_city, name='load_city'),
    path('load-city-list/', views.load_city_list, name='load_city_list'),
]
