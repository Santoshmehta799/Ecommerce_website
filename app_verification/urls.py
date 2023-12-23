from django.urls import path
from app_verification import views


app_name="app_verification"

urlpatterns = [
    path('', views.verification_home, name="verification_home"),
    path('gst-detail/', views.get_detail, name="get-detail"),
    path('general-detail/', views.general_detail, name="general-detail"),
]
