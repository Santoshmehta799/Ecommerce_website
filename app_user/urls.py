from django.urls import path
from app_user import views


app_name="app_user"

urlpatterns = [
    path('', views.auth_home, name="auth-name"),
    
    # Authentication
    path('auth/signup/', views.signup, name="auth-signup"),
    path('auth/signin/', views.signin, name="auth-signin"),

    # ajax
    path('email-check/', views.email_check_ajax, name='email_check_ajax'),

    # Forgot-Password
    path('forgot-password/', views.forgot_password, name="forgot-password"),

    path('auth/login-otp/', views.login_otp, name="auth-login-otp"),
    path('auth/sendmessage/', views.sendmessage, name="auth-sendmessage"),

    path('account-settings/', views.account_settings, name="account-settings"),
    path('reset-password/<slug:id>/<slug:otp>/', views.reset_password, name="reset-password"),
    path('confirmation-mail/<slug:id>/<slug:otp>/', views.confirmation_mail, name="confirmation-mail"),
    path('reset-new-password/', views.reset_new_password, name="reset-new-password"),
    path('reset-otp/', views.reset_otp, name="reset-otp"),
    path('forgot-mobile-otp/', views.forgot_mobile_otp, name="forgot-mobile-otp"),
    path('forgot-email-verify-page/', views.forgot_email_verify_page, name="forgot-email-verify-page"),



]
