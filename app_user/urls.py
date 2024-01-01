from django.urls import path
from app_user import views


app_name="app_user"
# https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
urlpatterns = [
    path('', views.auth_home, name="auth-name"),
    
    # Authentication
    path('auth/signup/', views.signup, name="auth-signup"),
    path('auth/signin/', views.signin, name="auth-signin"),
    path('auth/logout/', views.auth_logout, name="auth-logout"),
    path('emailVerification/<uidb64>/<token>/', views.activate, name='emailActivate'),

    # ajax
    path('email-check/', views.email_check_ajax, name='email_check_ajax'),
    path('except-user-email-check/', views.except_user_email_check_ajax, name='except_user_email_check_ajax'),
    path('phone-number-check/',views.phone_number_check,name="phone-number-check"),
    path('except-user-phone-number-check/',views.except_user_phone_number_check,name="except_user_phone_number_check"),
    path('auth/login-otp/', views.login_otp, name="auth-login-otp"),
    path('auth/signin-otp/', views.signin_otp, name="auth-signin-otp"),
    path('auth/verify-signin-otp/', views.verify_signin_otp, name="verify-auth-signin-otp"),

    # Forgot-Password
    path('forgot-password/', views.forgot_password, name="forgot-password"),

    path('auth/sendmessage/', views.sendmessage, name="auth-sendmessage"),

    path('account-settings/', views.account_settings, name="account-settings"),
    path('reset-password/<slug:id>/<slug:otp>/', views.reset_password, name="reset-password"),
    path('confirmation-mail/<slug:id>/<slug:otp>/', views.confirmation_mail, name="confirmation-mail"),
    path('reset-new-password/', views.reset_new_password, name="reset-new-password"),
    path('reset-otp/', views.reset_otp, name="reset-otp"),
    path('forgot-mobile-otp/', views.forgot_mobile_otp, name="forgot-mobile-otp"),
    path('forgot-email-verify-page/', views.forgot_email_verify_page, name="forgot-email-verify-page"),


    # profile 
    path('profile/', views.profile, name="profile"),
]
