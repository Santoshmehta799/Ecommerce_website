from django.urls import path
from app_inventory import views



app_name="app_inventory"

urlpatterns=[
    path('', views.inventory, name="inventory"),
    path('index/', views.inventory2, name="inventory_home2"),
    # add
    path('add/basic-info/', views.add_inventory_step_1, name="add_inventory_step_1"),
    path('add/variants/<uuid:product_id>/', views.add_inventory_step_2, name="add_inventory_step_2"),
    path('add/more-info/<uuid:product_id>/', views.add_inventory_step_3, name="add_inventory_step_3"),
    path('add/pricing/<uuid:product_id>/', views.add_inventory_step_4, name="add_inventory_step_4"),
    path('add/shipping/<uuid:product_id>/', views.add_inventory_step_5, name="add_inventory_step_5"),
    # edit
    path('edit/basic-info/<uuid:product_id>/', views.edit_inventory_step_1, name="edit_inventory_step_1"),
    path('edit/variants/<uuid:product_id>/', views.edit_inventory_step_2, name="edit_inventory_step_2"),
    path('edit/more-info/<uuid:product_id>/', views.edit_inventory_step_3, name="edit_inventory_step_3"),
    path('edit/pricing/<uuid:product_id>/', views.edit_inventory_step_4, name="edit_inventory_step_4"),
    path('edit/shipping/<uuid:product_id>/', views.edit_inventory_step_5, name="edit_inventory_step_5"),
    # Ajax load
    path('add/load-subcategory/',views.load_subcategory, name='load_subcategory'),  
    # path('add/', views.add_inventory, name="add_inventory"),
]
