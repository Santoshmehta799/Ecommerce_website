from django.urls import path
from app_inventory import views



app_name="app_inventory"

urlpatterns=[
    path('', views.inventory, name="inventory_home"),
    path('add/step-1/', views.add_inventory_step_1, name="add_inventory_step_1"),
    path('add/step-2/', views.add_inventory_step_2, name="add_inventory_step_2"),
    path('add/step-3/', views.add_inventory_step_3, name="add_inventory_step_3"),
    path('add/step-4/', views.add_inventory_step_4, name="add_inventory_step_4"),
    path('add/step-5/', views.add_inventory_step_5, name="add_inventory_step_5"),
    # path('add/', views.add_inventory, name="add_inventory"),
]
