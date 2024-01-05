from django.urls import path
from app_inventory import views



app_name="app_inventory"

urlpatterns=[
    path('', views.inventory, name="inventory_home"),
    path('add/step-1/', views.add_inventory_step_1, name="add_inventory_step_1"),
    path('add/step-2/', views.add_inventory_step_2, name="add_inventory_step_2"),
    # path('add/', views.add_inventory, name="add_inventory"),
]
