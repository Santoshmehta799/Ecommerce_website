from django.urls import path
from app_verification import views


app_name="app_verification"

urlpatterns = [
    path('', views.verification_home, name="verification_home"),
    path('gst-detail/', views.get_detail, name="get-detail"),
    path('general-detail/', views.general_detail, name="general-detail"),

    # ajax
    path('gst-check/',views.gst_check,name="gst-check"),
    path('except-user-gst-check/', views.except_user_gst_check, name="except_user_gst_check"),
]
