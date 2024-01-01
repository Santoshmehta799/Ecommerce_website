from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from app import settings
from app_inventory.models import PickUpWarehouseLocation
from app_user.forms.auth import LoginForm, RegisterForm
from app_verification.methods import bank_details_verification, cin_verification_step, generate_otp, pan_verification_step, registration_otp_send, update_gst_verification_step
from app_user.methods.auth import auth_login
from app_user.models import ProfileSettings, User
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

from app_verification.models import BankVerification, CompanyAddressDetail, CompanyBasicDetail, GstDetail, PanCinDetails, TempPhoneVerified, UserPhoneVerified
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
                messages.success(request,f"Welcome <b>{username}</b>.")
                next_url = request.GET.get("next")
                if next_url:
                    # print('enter hear...')
                    return redirect(next_url)
                print('enter else', next_url)
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
    user = request.user

    if request.method == 'POST':
        print(request.POST)
        form_model_type = request.POST.get('form_model_type')
        user = request.user
        
        if form_model_type == 'account_info_model':
            try:
                first_name = request.POST.get('first_name', None)
                ph_number = request.POST.get('mobile_number')
                password = request.POST.get('password')
                email = request.POST.get('email')

                account_info_model_status = False
                user_obj = User.objects.get(id=user.id)
                user_obj.first_name = first_name
                phone_verified_obj = UserPhoneVerified.objects.get(user_id=user.id)

                if user_obj.email != email.lower():
                    user_obj.email = email
                    user_obj.username = email
                    account_info_model_status = True
                if user_obj.show_password != password:
                    user_obj.set_password(password)
                    user_obj.show_password = password
                    account_info_model_status = True
                if phone_verified_obj.ph_number != ph_number:
                    phone_verified_obj.ph_number = ph_number
                    account_info_model_status = True
                user_obj.save()
                phone_verified_obj.save()

                if account_info_model_status == True:
                    return redirect('app_user:auth-logout')
                return redirect('app_user:profile')
            except Exception as e:
                error = f"Error: {e}"
            
        if form_model_type == 'seller_info_model':
            company_name = request.POST.get('company_name',None)
            state = request.POST.get('state')
            city = request.POST.get('city')
            pin_code = request.POST.get('pincode')
            address = request.POST.get('address')
            company_gst_number = request.POST.get('company_gst_number')
            document_type = request.POST.get('document_type')
            documnet_id = request.POST.get('documnet_id')
            about_brand = request.POST.get('about_brand')
            seller_info_model_status = True

            if company_name:
                company_details_obj, company_details_created = CompanyBasicDetail.objects.get_or_create(
                    user=user,company_name=company_name)
                company_details_obj.about_brand = about_brand
                company_details_obj.save()

            compnay_address_obj, compnay_address_created = CompanyAddressDetail.objects.get_or_create(
                user=user, city_id=city, state_id=state)
            compnay_address_obj.address_line_1 = address
            compnay_address_obj.pin_code = pin_code
            compnay_address_obj.save()

            user_gst_details_obj = GstDetail.objects.get(user=user)
            if user_gst_details_obj.company_gst_number != company_gst_number:
                gst_status, gst_msg = update_gst_verification_step(company_gst_number, request)
                if gst_status != True:
                    error = gst_msg
                    seller_info_model_status = False

            if seller_info_model_status != False:
                if document_type == PanCinDetailEnums.PAN:
                    pan_status, pan_msg = pan_verification_step(documnet_id, request)
                    if pan_status != True:
                        error = pan_msg
                        seller_info_model_status = False
                    
                if document_type == PanCinDetailEnums.CIN:
                    cin_status, cin_msg = cin_verification_step(documnet_id, request)
                    if cin_status != True:
                        error = cin_msg
                        seller_info_model_status = False
                else:
                    seller_info_model_status = False

            return redirect('app_user:profile')


        if form_model_type == 'account_setting_model':
            order_handling_time = request.POST.get('order_handling_time')
            order_cutt_off_time = request.POST.get('order_cutt_off_time')
            receive_order_update_whatsapp = request.POST.get('receive_order_update_whatsapp')
            receive_order_update_call = request.POST.get('receive_order_update_call')
            receive_order_update_email = request.POST.get('receive_order_update_email')
            receive_payment_update_whatsapp = request.POST.get('receive_payment_update_whatsapp')
            receive_payment_update_call = request.POST.get('receive_payment_update_call')
            receive_payment_update_email = request.POST.get('receive_payment_update_email')
            try:
                profile_setting_obj, profile_setting_created = ProfileSettings.objects.get_or_create(
                    user=user)
                profile_setting_obj.order_handling_time=order_handling_time
                profile_setting_obj.order_cutt_off_time=order_cutt_off_time
                profile_setting_obj.receive_order_update_whatsapp=True if receive_order_update_whatsapp else False
                profile_setting_obj.receive_order_update_call=True if receive_order_update_call else False
                profile_setting_obj.receive_order_update_email=True if receive_order_update_email else False
                profile_setting_obj.receive_payment_update_whatsapp=True if receive_payment_update_whatsapp else False
                profile_setting_obj.receive_payment_update_call=True if receive_payment_update_call else False
                profile_setting_obj.receive_payment_update_email=True if receive_payment_update_email else False
                profile_setting_obj.save()
                return redirect('app_user:profile')
            except Exception as e:
                error = f"Error: {e}"


        if form_model_type == 'bank_account_info_model':
            account_holder = request.POST.get('account_holder', None)
            account_number = request.POST.get('account_number', None)
            ifsc_code = request.POST.get('ifsc', None)
            # print('======>>>',account_holder,account_number,ifsc_code)
            if account_holder and account_number and ifsc_code:
                bank_details_status, bank_details_msg = bank_details_verification(account_holder, 
                        account_number, ifsc_code, request)
                if bank_details_status == True:
                    return redirect('app_user:profile')
                else:
                    error=bank_details_msg



        if form_model_type == 'delete_warehouse_info_model':
            delete_warehouse_id = request.POST.get('delete_warehouse_id')
            try:
                pickup_obj = PickUpWarehouseLocation.objects.filter(id=delete_warehouse_id).delete()
                return redirect('app_user:profile')
            except PickUpWarehouseLocation.DoesNotExist:
                error = "Warehouse Doesnot Exist."

        if form_model_type == 'add_warehouse_info_model':
            location_name = request.POST.get('location_name')
            plot_no = request.POST.get('plot_no')
            street = request.POST.get('street')
            state = request.POST.get('state')
            city = request.POST.get('city')
            landmark = request.POST.get('landmark')
            pin_code = request.POST.get('pin_code')
            print('add_warehouse_info_model')
            try:
                pickup_obj = PickUpWarehouseLocation()
                pickup_obj.user = user
                pickup_obj.plot_no = plot_no
                pickup_obj.location_name = location_name
                pickup_obj.street = street
                pickup_obj.landmark = landmark
                pickup_obj.state_id = state
                pickup_obj.city_id = city
                pickup_obj.pin_code = pin_code
                pickup_obj.save()
                return redirect('app_user:profile')
            except Exception as e:
                error = f"Error : {e}"


        if form_model_type == 'edit_warehouse_info_model':
            edit_warehouse_id = request.POST.get('edit_warehouse_id')
            location_name = request.POST.get('location_name')
            plot_no = request.POST.get('plot_no')
            street = request.POST.get('street')
            state = request.POST.get('state')
            city = request.POST.get('city')
            landmark = request.POST.get('landmark')
            pin_code = request.POST.get('pin_code')
            print('edit_warehouse_info_model', edit_warehouse_id)
            try:
                pickup_obj = PickUpWarehouseLocation.objects.get(id=edit_warehouse_id)
                pickup_obj.plot_no = plot_no
                pickup_obj.location_name = location_name
                pickup_obj.street = street
                pickup_obj.landmark = landmark
                pickup_obj.state_id = state
                pickup_obj.city_id = city
                pickup_obj.pin_code = pin_code
                pickup_obj.save()
                return redirect('app_user:profile')
            except Exception as e:
                error = f"Error : {e}"

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







    
