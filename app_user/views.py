from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from app import settings
from app_user.forms.auth import LoginForm, RegisterForm
from app_verification.methods import generate_otp, registration_otp_send
from app_user.methods.auth import auth_login
from app_user.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from app_user.tokens import account_activation_token
from django.contrib import auth
from app_dashboard.models import Cities, States

from app_verification.models import TempPhoneVerified, UserPhoneVerified
from common.enums import OrderCuttOffTime, OrderHandlingTimeEnums, PanCinDetailEnums, UserAuthIdentifierType, UserStatusEnums
# Create your views here.


def auth_home(request):
    return HttpResponse("hello , testing!")

def signin(request):
    # http://127.0.0.1:8000/dashboard/
    # http://127.0.0.1:8000/user/auth/logout
    success = ""
    error = ""
    if request.user and request.user.is_authenticated:
        return redirect('app_dashboard:dashboard-page')
    
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            status, msg = auth_login(request, username, password)
            # print('statusv-->',status)
            if status == True:
                next_url = request.GET.get("next")
                if next_url:
                    # print('enter hear...')
                    messages.success(request,f"Welcome <b>{username}</b>.")
                    return redirect(next_url)
                print('enter else', next_url )
                messages.success(request,f"Welcome <b>{username}</b>.")
                return redirect('app_verification:get-detail')
            else:
                error = msg
    context = {
        'error' : error,
        'success' : success,
        'form' : form,
    }
    return render(request, 'app_user/signin.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(request, f"Thank you for your email confirmation. Now you can login your account. Go <a href='/'>Home</a>." )
        return redirect('app_user:auth-signin')
    else:
        return HttpResponse('Activation link is invalid!')

def signin_otp(request):
    status = False
    msg = "invalid request."
    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        temp_phone_verified, created = TempPhoneVerified.objects.get_or_create(
            ph_number=contact_number)
        if temp_phone_verified:
            otp_generated = generate_otp()
            if otp_generated:
                print("OTP ->", otp_generated)
                if registration_otp_send(contact_number, otp_generated):
                    temp_phone_verified.otp = otp_generated
                    temp_phone_verified.otp_send = True
                    temp_phone_verified.is_verified = False
                    temp_phone_verified.save()
                    status = True
                    msg = "otp successfully sent."
                else:
                    msg = "failed to send otp using api."
                    status = False
            else:
                msg = "failed to generate otp."
                status = False
        else:
            msg = "obj not created check query"
            status = False
    return JsonResponse({'status':status, 'msg':msg})

def verify_signin_otp(request):
    status = False
    msg = "invalid request."
    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        otp_number = request.POST.get('otp_number')
        temp_phone_verified = TempPhoneVerified.objects.filter(ph_number=contact_number, otp=otp_number,
            otp_send=True)
        if len(temp_phone_verified) > 0:
            update_temp_phone_verified = temp_phone_verified.get(ph_number=contact_number)
            update_temp_phone_verified.is_verified = True
            update_temp_phone_verified.save()
            status = True
            msg = "otp verification completed."
        else:
            msg = "verification failed due to invalid otp. please send try again."
            status = False
    return JsonResponse({'status':status, 'msg':msg})

        

def signup(request):
    success = ""
    error = ""
    if request.method == "GET":
        return redirect('/?#Register')
    context = {
        'error' : error,
        'success' : success,
    }
    return render(request, 'app_user/signup.html', context)


def email_check_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        user_exist = User.objects.filter(email = email)
        if user_exist.count() > 0:
            return JsonResponse(False, safe=False)
        else:
            return JsonResponse(True, safe=False)
        
def except_user_email_check_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        current_user_email = request.user.email.lower() if request.user.is_authenticated else None
        user_exist = User.objects.filter(email=email).exclude(email=current_user_email)

        if user_exist.exists():
            return JsonResponse(False, safe=False)
        else:
            return JsonResponse(True, safe=False)
        

# @login_required(login_url = settings.LOGIN_URL)
def phone_number_check(request):
    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        print(contact_number)
        contact_exist = UserPhoneVerified.objects.filter(Q(ph_number=contact_number))
        if len(contact_exist)< 1:
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)


@login_required
def except_user_phone_number_check(request):
    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')

        try:
            current_user_phone = UserPhoneVerified.objects.get(user=request.user)
        except ObjectDoesNotExist:
            current_user_phone = None

        contact_exist = UserPhoneVerified.objects.filter(ph_number=contact_number).exclude(pk=current_user_phone.pk if current_user_phone else None)

        if len(contact_exist) < 1:
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
    return render(request, 'app_user/mail/forgot_mobile_otp.html')

def forgot_email_verify_page(request):
    return render(request, 'app_user/mail/forgot_email_verify_page.html')

@login_required()
def profile(request):
    success = ""
    error = ""

    if request.method == 'POST':
        print(request.POST)
        form_model_type = request.POST.get('form_model_type')
        if form_model_type == 'account_info_model':
            print('account_info_model')
            first_name = request.POST.get('first_name')
            print("============>>>", form_model_type)
            ph_number = request.POST.get('ph_number')
            exist_ph_number = UserPhoneVerified.objects.filter(ph_number=ph_number).exists()
            email = request.POST.get('email')
            exist_ph_number = User.objects.filter(email=email).exists()
            password = request.POST.get('password')
            print('====--->',first_name, ph_number, email, password)
            
        if form_model_type == 'seller_info_model':
            print('seller_info_model')
        if form_model_type == 'account_setting_model':
            print('account_setting_model')
        if form_model_type == 'bank_account_info_model':
            print('bank_account_info_model')
        if form_model_type == 'edit_warehouse_info_model':
            print('edit_warehouse_info_model')
        if form_model_type == 'delete_warehouse_info_model':
            print('delete_warehouse_info_model')
        if form_model_type == 'add_warehouse_info_model':
            print('add_warehouse_info_model')

    

    context = {
        "success": success,
        "error": error,
        "pan_cin_choices" : PanCinDetailEnums.choices,
        "state_obj": States.objects.filter(country__name='INDIA').select_related('country'),
        "city_obj" : Cities.objects.filter(state__country__name='INDIA').select_related('state__country'),
        "order_cut_off_time": OrderCuttOffTime.choices, 
        "order_handing_time" : OrderHandlingTimeEnums.choices,
        
    }
    return render(request, 'app_user/profile.html', context)


def auth_logout(request):
    logout(request)
    return redirect('app_user:auth-signin')







    
