from django.urls import path
from app_inventory import views



app_name="app_inventory"

urlpatterns=[
    path('', views.inventory, name="inventory_home")
]