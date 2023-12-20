from django.urls import path
from app_user import views


app_name="app_user"

urlpatterns = [
    path('', views.auth_home, name="auth-name"),
    path('auth/login/', views.auth_home, name="auth-login"),
]
