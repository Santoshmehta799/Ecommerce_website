from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from app_user import forms as user_forms, methods as user_methods
from app_user.models import User
from django.contrib import messages
from django.db.models import Q
# Create your views here.


def auth_home(request):
    return HttpResponse("hello , testing!")

def signin(request):
    return render(request, 'app_user/signin.html')

def signup(request):
    success = ""
    error = ""
    form = user_forms.auth.RegisterForm(request.POST or None)
    if request.method == "GET":
        return redirect('/?#Register')

    if request.method == 'POST':
        email = request.POST['email']
        if form.is_valid():
            try:
                is_user_exit = User.objects.get(email=email)
            except:
                is_user_exit = ''

            if not is_user_exit:
                try:
                    user_methods.auth.admin_register_methods(request,form)
                    messages.success(request,'Registration sucessfully done!')
                    return redirect('crm_app:home')
                except:
                    error = "User with this email already exists."
            else:
                error = "User with this email already exists."

    context = {
        'error' : error,
        'success' : success,
        'form' :form,
    }
    return render(request, 'app_user/signup.html', context)


def email_check_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        user_exist = User.objects.filter(Q(email=email))
        if user_exist:
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)
        

def forgot_password(request):
    return render(request, 'app_user/forgot_password.html')

def login_otp(request):
    return render(request, 'app_user/login_otp.html')

def sendmessage(request):
    return render(request, 'app_user/sendmessage.html')

def account_settings(request):
    return render(request, 'app_user/general_detail.html')

def reset_password(request):
    return render(request, 'app_user/reset_password.html')

def confirmation_mail(request):
    return render(request, 'app_user/confirmation_mail.html')

def reset_new_password(request):
    return render(request, 'app_user/reset_new_password.html')

def reset_otp(request):
    return render(request, 'app_user/reset_otp.html')

def forgot_mobile_otp(request):
    return render(request, 'app_user/email-templates/forgot_mobile_otp.html')

def forgot_email_verify_page(request):
    return render(request, 'app_user/email-templates/forgot_email_verify_page.html')





    
