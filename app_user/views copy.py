from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from app import settings
from app_inventory.models import Category, PickUpWarehouseLocation, Product, ProductType, ShippingDetails
from app_user.forms.auth import LoginForm, RegisterForm
from app_verification.methods import bank_details_verification, bank_excel_details_verification, cin_excel_verification_step, cin_verification_step, generate_otp, gst_excel_verification_step, pan_excel_verification_step, pan_verification_step, registration_otp_send, update_gst_verification_step
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
import pandas as pd
from app_verification.models import BankVerification, CompanyAddressDetail, CompanyBasicDetail, GstDetail, PanCinDetails, RepresentativeDetail, TempPhoneVerified, UserPhoneVerified
from common.enums import OrderCuttOffTimeEnums, OrderHandlingTimeEnums, PanCinDetailEnums, UserAuthIdentifierType, UserStatusEnums
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
            current_user_phone = UserPhoneVerified.objects.get(seller=request.user)
        except ObjectDoesNotExist:
            current_user_phone = None

        contact_exist = UserPhoneVerified.objects.filter(ph_number=contact_number).exclude(pk=current_user_phone.pk if current_user_phone else None)

        if len(contact_exist) < 1:
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)
        

def forgot_password(request):
    success = ""
    error =""
    if request.method == 'POST':
        print("=-=============")
        mobile_number = request.POST.get('mobile_number', None)
        print("======",mobile_number)
        if mobile_number:
            print('mobile_number ->', mobile_number)
            try:
                user_phone_verified = UserPhoneVerified.objects.get(ph_number=mobile_number)
                if user_phone_verified:
                    otp_generated = generate_otp()
                    if otp_generated:
                        print("OTP ->", otp_generated)
                        if registration_otp_send(mobile_number, otp_generated):
                            user_phone_verified.otp = otp_generated
                            user_phone_verified.otp_send = True
                            user_phone_verified.reset_password_verify = False
                            user_phone_verified.save()
                            # request.session.get('verify_ph_number' ,user_phone_verified.ph_number)
                            request.session['verify_ph_number'] = user_phone_verified.ph_number
                            messages.success(request, 'otp successfully sent.')
                            return redirect('app_user:forgot-mobile-otp')
                        else:
                            error = "failed to send otp using api."
                    else:
                        error = "failed to generate otp."
                else:
                    error = "phone number does not match"
            except Exception as e:
                error = f"An error occurred: mobile number does not match"
                print(f"Error: {str(e)}")
        else:
            error = "phone enter phone number"


    context={
        "error": error,
        "success": success
    }
    return render(request, 'app_user/forgot_password.html', context)

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
    success = ""
    error =""
    verify_ph_number_session = request.session.get('verify_ph_number')
    if not verify_ph_number_session:
        return JsonResponse({'data': 'invalid request'})
    
    if request.method == 'POST':
        new_password = request.POST.get('password')
        phone_number_verified_obj = UserPhoneVerified.objects.filter(ph_number=verify_ph_number_session)
        if phone_number_verified_obj:
            ph_number_obj = phone_number_verified_obj.first()
            ph_number_obj.seller.set_password(new_password)
            ph_number_obj.seller.show_password = new_password
            ph_number_obj.seller.save()
            verify_ph_number_session = request.session.pop('verify_ph_number', None)
            return redirect('app_user:auth-signin')
        else:
            error = "In valid Credentials."

    context={
        "error": error,
        "success": success
    }
    return render(request, 'app_user/reset_new_password.html',context)

def reset_otp(request):
    return render(request, 'app_user/reset_otp.html')


def forgot_mobile_otp(request):
    success = ""
    error =""
    verify_ph_number_session = request.session.get('verify_ph_number')
    print('session_data', verify_ph_number_session)
    if request.method == 'POST':
        otp_verify = request.POST.get('otp')
        user_otp_verify = UserPhoneVerified.objects.filter(otp=otp_verify, 
            ph_number=verify_ph_number_session)
        if user_otp_verify:
            user_phone_verified = user_otp_verify.first()
            user_phone_verified.reset_password_verify = True
            user_phone_verified.save()
            return redirect('app_user:reset-new-password')
        else:
            error = "invalid otp not Found."

    context={
        "error": error,
        "success": success
    }
    return render(request, 'app_user/mail/forgot_mobile_otp.html', context)

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
                phone_verified_obj = UserPhoneVerified.objects.get(seller=user.id)

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
                error = f"Error 11: {e}"
            
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
                    seller=user, company_name=company_name)
                company_details_obj.about_brand = about_brand
                company_details_obj.save()

            compnay_address_obj, compnay_address_created = CompanyAddressDetail.objects.get_or_create(
                seller=user, city_id=city, state_id=state)
            compnay_address_obj.address_line_1 = address
            compnay_address_obj.pin_code = pin_code
            compnay_address_obj.save()

            user_gst_details_obj = GstDetail.objects.get(seller=user)
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
                    seller=user)
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
                pickup_obj.seller = user
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
        "order_cut_off_time": OrderCuttOffTimeEnums.choices, 
        "order_handing_time" : OrderHandlingTimeEnums.choices,
        
    }
    return render(request, 'app_user/profile.html', context)


def auth_logout(request):
    logout(request)
    return redirect('app_user:auth-signin')



@login_required()
def category_xlsx_import(request):
    user = request.user

    if user.is_superuser:
        base_url = settings.BASE_DIR
        category_file_location = f'{base_url}'+'/static/seventh-square/assets/xlsx/category_data.xlsx'
        subcategory_file_location = f'{base_url}'+'/static/seventh-square/assets/xlsx/subcategory_data.xlsx'
        inventory_file_location = f'{base_url}'+'/static/seventh-square/assets/xlsx/inventory_data.xlsx'
        one_to_one_file_location = f'{base_url}'+'/static/seventh-square/assets/xlsx/one_to_one_field.xlsx'


        cat_df = pd.read_excel(category_file_location)
        cat_df_dict = cat_df.to_dict(orient='index')
        for cat_key, cat_value in cat_df_dict.items():
            category_obj, created = Category.objects.get_or_create(name=cat_value['name'], defaults={
                'slug':cat_value['slug']
            })
            

            df = pd.read_excel(subcategory_file_location)
            df_dict = df.to_dict(orient='index')
            for key, value in df_dict.items():
                if cat_value['id'] == value['category_id']:
                    if value['commision_type'] == 'commision_percentage':
                        value['commision_type'] = 'commission_percentage'

                    product_type_obj, created = ProductType.objects.get_or_create(category=category_obj, name=value['name'],
                        defaults={
                            'slug':value['slug'],
                            'commission_type':value['commision_type'],
                            'commission_value':value['commision_value'],
                            'returnable_product':value['returnable_product']
                        })
            
                    inventory_df = pd.read_excel(inventory_file_location)
                    inventory_df_dict = inventory_df.to_dict(orient='index')

                    one_to_one_df = pd.read_excel(one_to_one_file_location)
                    one_to_one_df_dict = one_to_one_df.to_dict(orient='index')

                    final_list = {}
                    for inventory_key, inventory_value in inventory_df_dict.items():
                        print("-----upper=-->",inventory_value['variant_default'])
                        username = None
                        # for one_to_one_key, one_to_one_value in one_to_one_df_dict.items():
                        #     pass
                            # if inventory_value['account_id'] == one_to_one_value['user_id']:
                            #     username=one_to_one_value['username']

                        varient_id = inventory_value['variant_product_id']

                        if str(varient_id) in final_list:
                            print("-----if-->",inventory_value['variant_default'])
                            # print("------varient----==>",inventory_value['variant_default'])
                            if inventory_value['variant_default'] == True:
                                print("-------------id---")
                                final_list[str(varient_id)]['main_varient'].append(inventory_value)
                            else:
                                print("--------------else--")
                                final_list[str(varient_id)]['sub_varient'].append(inventory_value)

                            # print(inventory_value['variant_default'])
                            
                        else:
                            final_list[str(varient_id)] = {
                                'main_varient' : [],
                                'sub_varient' : []
                            }

                    # print("-------------??>>",final_list)
                        # if inventory_value['var_added'] == True:
                        #     print('with varient product')
                        #     if inventory_value['variant_default'] == True:
                        #         varient_id = inventory_value['variant_product_id']
                        #         final_list['main_varient'] = main_varient.append(inventory_value)
                        #         for inner_inventory_key, inner_inventory_value in inventory_df_dict.items():
                        #             if inventory_value['var_added'] == True:
                        #                 if inventory_value['variant_default'] == False and varient_id==inner_inventory_value['variant_product_id']:
                        #                     final_list['sub_varient'] = sub_varient.append(inner_inventory_value)



                        #             # product_obj, created = Product.objects.get_or_create(
                        #             #     seller__username = one_to_one_value['username'],
                        #             #     category = category_obj,
                        #             #     product_type =product_type_obj,
                        #             #     country_of_origin__name = inventory_value['countryOfOrigin'],
                        #             #     defaults={
                        #             #         'about_the_brand':inventory_value['aboutBrand'],
                        #             #         'product_brand':inventory_value['brand_name'],
                        #             #         'guarantee':inventory_value['guarantee'],
                        #             #         'warranty': inventory_value['warranty'],
                        #             #         'shipping_include':inventory_value['incl_shipping'],
                        #             #         'serviced_regions':inventory_value['servicedRegions'],
                        #             #         'usage':inventory_value['aboutUsage'],
                        #             #         'storage':inventory_value['aboutStorage'],
                        #             #         'installation':inventory_value['aboutInstallation'],
                        #             #         'components_per_unit':inventory_value['components'],
                        #             #         'packaging_size':inventory_value['packagingSize'],
                        #             #         'material':inventory_value['material'],
                        #             #         'description':inventory_value['description'],
                        #             #         'is_active':inventory_value['inventoryStatus'],

                        #             #     }
                        #             # )
                        # else:
                        #     final_list['main_varient'] = main_varient.append(inventory_value)

            # for arrange_product in final_list:
            #     print('final_list ->',arrange_product)        
                    



    return HttpResponse("Excel file has successfully imported")




@login_required()
def one_to_one_xlsx_import(request):
    '''
    0 {'user_id': 5, 'gst_number': '09AGXPG6194L1ZE', 'username': '9149100488', 'email': 'hritikgoyal19@gmail.com', 'email_verification_code': 45836, 'gst_in': True, 'company_name': 'GOYAL UDYOG', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': '12345678', 'password': 'pbkdf2_sha256$260000$S7o4devzZnqjUKr4nCUWCZ$gKRrlno+LIpzWSNTmSOZMf+jL+mMVV8hkEI81K9+5JE=', 'last_login': Timestamp('2023-10-16 15:56:07.195000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-09-25 13:57:04.045000'), 'mobile_number': 9149100488.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': ' ALIGARH ', 'state': 'UTTAR PRADESH', 'records_for': 'GST_API_User_data', 'id': 17.0, 'User_id': 5.0, 'Legal_Name_of_Business': 'RAJ KUMAR GOYAL', 'State_Jurisdiction': 'Aligarh Sector-1', 'Date_of_Registration': '13/07/2017', 'Constitution_of_Business': 'Proprietorship', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Wholesale Business', 'Supplier of Services', 'Retail Business', 'Factory / Manufacturing', 'Recipient of Goods or Services']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'UP1462', 'Trade_Name': 'GOYAL UDYOG', 'Additional_place_of_business_address': nan, 'Street': 'RAMGHAT ROAD', 'Location': 'ALIGARH', 'state_name': 'Uttar Pradesh', 'floor_nbr': 'TALA NAGARI', 'pin_code': 202001.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': 'Uttar Pradesh', 'Pin_Code_repeat': 202001.0, 'created_at': Timestamp('2023-10-16 15:57:27.346000'), 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    1 {'user_id': 71, 'gst_number': nan,              'username': '9958655595', 'email': 'singhabhi.281988@gmail.com', 'email_verification_code': 95159, 'gst_in': False, 'company_name': nan, 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': 'badboyabhi28', 'password': 'pbkdf2_sha256$260000$4KQt7lYVKiY8kJqRx274mE$FMCdIyT4nlrO8ghHGwQGOeJR1cGY8A2Vz5KQBKWdc5w=', 'last_login': Timestamp('2023-12-21 06:08:58.539000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-12-21 06:08:58.429000'), 'mobile_number': 9958655595.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': False, 'general_check': False, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': 'NONE', 'state': 'NONE', 'records_for': 'Account', 'id': nan, 'User_id': nan, 'Legal_Name_of_Business': nan, 'State_Jurisdiction': nan, 'Date_of_Registration': nan, 'Constitution_of_Business': nan, 'Taxpayer_type': nan, 'Nature_of_Business_Activity': nan, 'GSTN_status': nan, 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': nan, 'Trade_Name': nan, 'Additional_place_of_business_address': nan, 'Street': nan, 'Location': nan, 'state_name': nan, 'floor_nbr': nan, 'pin_code': nan, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': nan, 'Pin_Code_repeat': nan, 'created_at': NaT, 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    2 {'user_id': 31, 'gst_number': '05AALCB1359F1ZU', 'username': '9760933646', 'email': 'aman123kalra@gmail.com', 'email_verification_code': 24936, 'gst_in': True, 'company_name': 'Black Meets Gold', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': '9760933646', 'password': 'pbkdf2_sha256$260000$MS7iYlDywqJNSRjfSBgjvu$s/FMzq9+K2rgPmocKl91NKhkXFekJX9nSaJV0IV11GM=', 'last_login': Timestamp('2023-11-17 10:11:08.830000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-11-17 10:11:08.555000'), 'mobile_number': 9760933646.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': ' DEHRADUN ', 'state': 'UTTARAKHAND', 'records_for': 'GST_API_User_data', 'id': 26.0, 'User_id': 31.0, 'Legal_Name_of_Business': 'BLACK MEETS GOLD PRIVATE LIMITED', 'State_Jurisdiction': 'Dehradun - Sector 3', 'Date_of_Registration': '09/11/2022', 'Constitution_of_Business': 'Private Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Office / Sale Office', 'Supplier of Services']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'UT006', 'Trade_Name': 'BLACK MEETS GOLD PRIVATE LIMITED', 'Additional_place_of_business_address': nan, 'Street': 'Nemi Road', 'Location': 'Dehradun', 'state_name': 'Uttarakhand', 'floor_nbr': nan, 'pin_code': 248001.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': 'Uttarakhand', 'Pin_Code_repeat': 248001.0, 'created_at': Timestamp('2023-11-17 10:21:12.660000'), 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    3 {'user_id': 2, 'gst_number': '36AAACR4849R1CX', 'username': '8200525530', 'email': 'ravichovatiya120@gmail.com', 'email_verification_code': 538902, 'gst_in': True, 'company_name': 'tril company', 'company_verification_type': 'PAN', 'company_verification_number': nan, 'password_text': '12345', 'password': 'pbkdf2_sha256$260000$tZPBaC67StJqCGx97lvYqH$wGOLifRYagosAafiYpDrdQssaCulFpwtncfUMnxzP2c=', 'last_login': Timestamp('2024-01-25 08:57:22.844000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-09-20 13:34:12.217000'), 'mobile_number': 8200525530.0, 'is_mobile_number_verified': True, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': True, 'receive_payment_whatsapp': True, 'receive_payment_call': True, 'receive_payment_email': True, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': True, 'gst_details_done': True, 'general_check': True, 'order_handling_time': 4.0, 'order_cutoff_time': '07:00', 'city': 'Surat', 'state': 'Gujarat', 'records_for': 'GST_API_User_data', 'id': 2.0, 'User_id': 2.0, 'Legal_Name_of_Business': nan, 'State_Jurisdiction': nan, 'Date_of_Registration': nan, 'Constitution_of_Business': nan, 'Taxpayer_type': nan, 'Nature_of_Business_Activity': nan, 'GSTN_status': nan, 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': nan, 'Trade_Name': nan, 'Additional_place_of_business_address': nan, 'Street': nan, 'Location': nan, 'state_name': nan, 'floor_nbr': nan, 'pin_code': nan, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': nan, 'Pin_Code_repeat': nan, 'created_at': Timestamp('2023-09-20 13:37:22.535000'), 'Data Type': 'Address Data', 'account': 2.0, 'address': 'lambe hanuman road', 'pincode': 395006.0, 'latitude': nan, 'longitude': nan, 'isAddressVerified': 0.0, 'addressType': 'COMPANY', 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    4 {'user_id': 1, 'gst_number': '24AAACR5055K1ZD', 'username': 'aditya',     'email': 'aditya@gmail.com', 'email_verification_code': 647072, 'gst_in': True, 'company_name': 'dwe', 'company_verification_type': 'CIN', 'company_verification_number': nan, 'password_text': nan, 'password': 'pbkdf2_sha256$260000$gOcBEB0U2gAzFsG85KWnub$uCVHrxLCuhY/7+ilq6QabaKdIxaPblwNlbnN/LGuOc4=', 'last_login': Timestamp('2024-01-25 09:04:05.573000'), 'is_superuser': True, 'is_active': True, 'is_staff': True, 'date_joined': Timestamp('2023-09-20 13:32:09.240000'), 'mobile_number': nan, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': False, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': 'asdffasd', 'state': 'sdafasdf', 'records_for': 'GST_API_User_data', 'id': 1.0, 'User_id': 1.0, 'Legal_Name_of_Business': 'RELIANCE INDUSTRIES LIMITED', 'State_Jurisdiction': 'Ghatak 100 (Jamnagar)', 'Date_of_Registration': '01/07/2017', 'Constitution_of_Business': 'Public Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Factory / Manufacturing', 'Warehouse / Depot', 'Retail Business', 'Others', 'Office / Sale Office', 'Leasing Business', 'Works Contract']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'GJ100', 'Trade_Name': 'RELIANCE INDUSTRIES  LTD.', 'Additional_place_of_business_address': nan, 'Street': 'PO Motikhavdi', 'Location': 'Meghpar Padana Gagva', 'state_name': 'Gujarat', 'floor_nbr': nan, 'pin_code': 361140.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': 'Reliance industries Limited', 'State_name_repeat': 'Gujarat', 'Pin_Code_repeat': 361140.0, 'created_at': Timestamp('2023-12-15 05:02:32.392000'), 'Data Type': 'Address Data', 'account': 1.0, 'address': 'adfads', 'pincode': 395006.0, 'latitude': nan, 'longitude': nan, 'isAddressVerified': 0.0, 'addressType': 'COMPANY', 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    5 {'user_id': 21, 'gst_number': '09AAACL5727E1ZL', 'username': '7217011403', 'email': 'mamtarani@linklocks.com', 'email_verification_code': 11343, 'gst_in': True, 'company_name': 'Link Locks Private Limited', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': 'Mamta@2023', 'password': 'pbkdf2_sha256$260000$TFtuuNYC2Uea2KttDWL5ne$ASHKQsLLucK+C0ASJHT/nlW/cBorMJevIV26ULzZTQ8=', 'last_login': Timestamp('2023-12-08 10:31:46.765000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-10-20 05:16:58.960000'), 'mobile_number': 7217011403.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': ' DELHI ', 'state': 'DELHI', 'records_for': 'GST_API_User_data', 'id': 18.0, 'User_id': 21.0, 'Legal_Name_of_Business': 'LINK LOCKS PRIVATE LIMITED', 'State_Jurisdiction': 'Corporate Circle, Aligarh', 'Date_of_Registration': '01/07/2017', 'Constitution_of_Business': 'Private Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Factory / Manufacturing', 'Wholesale Business', 'Export', 'Supplier of Services', 'Import', 'Office / Sale Office', 'Warehouse / Depot', 'Recipient of Goods or Services', 'Retail Business']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'UP319', 'Trade_Name': 'M/S LINK LOCKS PVT. LTD.', 'Additional_place_of_business_address': nan, 'Street': 'CDF CHHERAT, ANUPSHAHR ROAD', 'Location': 'ALIGARH', 'state_name': 'Uttar Pradesh', 'floor_nbr': nan, 'pin_code': 202001.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': 'Uttar Pradesh', 'Pin_Code_repeat': 202001.0, 'created_at': Timestamp('2023-10-20 05:17:17.885000'), 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    6 {'user_id': 66, 'gst_number': '07AACCF7087P1ZX', 'username': '7303032131', 'email': 'ecom@foruselectric.com', 'email_verification_code': 72501, 'gst_in': True, 'company_name': 'Forus Electric Private Limited', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': 'Ecom@6565', 'password': 'pbkdf2_sha256$260000$2l6cQp2hIkKsY2N5Kp3qGn$V0OLBu1n7CrdLImhT1scfwAhIUNW/IHf8miI5JJBGPg=', 'last_login': Timestamp('2024-01-05 05:11:13.438000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-11-27 05:54:51.969000'), 'mobile_number': 7303032131.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': True, 'receive_order_call': True, 'receive_order_email': True, 'receive_payment_whatsapp': True, 'receive_payment_call': False, 'receive_payment_email': True, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': True, 'gst_details_done': True, 'general_check': True, 'order_handling_time': 0.0, 'order_cutoff_time': '17:00', 'city': ' DELHI ', 'state': 'DELHI', 'records_for': 'GST_API_User_data', 'id': 12.0, 'User_id': 66.0, 'Legal_Name_of_Business': 'FORUS ELECTRIC PRIVATE LIMITED', 'State_Jurisdiction': 'Ward 93', 'Date_of_Registration': '01/07/2017', 'Constitution_of_Business': 'Private Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Wholesale Business', 'Factory / Manufacturing', 'Retail Business', 'Warehouse / Depot']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'DL093', 'Trade_Name': 'FORUS ELECTRIC PRIVATE LIMITED', 'Additional_place_of_business_address': nan, 'Street': 'Power House Block B Phase 1 Road', 'Location': 'New Delhi', 'state_name': 'Delhi', 'floor_nbr': nan, 'pin_code': 110020.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': 'Delhi', 'Pin_Code_repeat': 110020.0, 'created_at': Timestamp('2023-11-27 05:56:58.692000'), 'Data Type': 'Bank Data', 'account': 66.0, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': 'FORUS ELECTRIC PRIVATE LIMITED', 'accountNumber': 71605003702.0, 'ifsc': 'ICIC0000716', 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': 'NO', 'date': Timestamp('2023-11-29 07:41:05.561000'), 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    7 {'user_id': 26, 'gst_number': '36AAACT2727Q1ZX', 'username': '8401296486', 'email': 'ravichovatiya121@gmail.com', 'email_verification_code': 27073, 'gst_in': True, 'company_name': 'test company testing', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': '1234', 'password': 'pbkdf2_sha256$260000$cCRQcWvV3uhLPv7LU9WCAa$obQwqd2cKidSI3eoIAVySGiSZBWQRgNgCZ01s1e3Wvs=', 'last_login': Timestamp('2024-01-24 06:59:06.656000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-10-31 11:09:23.539000'), 'mobile_number': 8401296486.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': ' SURAT ', 'state': 'GUJARAT', 'records_for': 'GST_API_User_data', 'id': 21.0, 'User_id': 26.0, 'Legal_Name_of_Business': 'TATA MOTORS LIMITED', 'State_Jurisdiction': 'MALKAJGIRI STU 2', 'Date_of_Registration': '01/07/2017', 'Constitution_of_Business': 'Public Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Office / Sale Office', 'Recipient of Goods or Services', 'Warehouse / Depot']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'TGC037', 'Trade_Name': 'TATA MOTORS LIMITED', 'Additional_place_of_business_address': nan, 'Street': 'Sardar Patel Road', 'Location': 'Hyderabad', 'state_name': 'Telangana', 'floor_nbr': '7th Floor, Gumidelli Towers Opp Shoppers Stop', 'pin_code': 500016.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': 'Cache Properties pvt ltd', 'State_name_repeat': 'Telangana', 'Pin_Code_repeat': 500016.0, 'created_at': Timestamp('2023-10-31 11:11:48.905000'), 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    8 {'user_id': 72, 'gst_number': nan,                'username': '9830373514', 'email': 'jishika0601@gmail.com', 'email_verification_code': 23342, 'gst_in': False, 'company_name': nan, 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': 'Mymom.678', 'password': 'pbkdf2_sha256$260000$9Hff0rT7yX9IpOmAMXMvgB$oqDtVIJkG22tZZKFwjlwEBViHS6R+4FSlzySCsMnPm0=', 'last_login': Timestamp('2023-12-28 12:00:40.672000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-12-28 12:00:40.535000'), 'mobile_number': 9830373514.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': False, 'general_check': False, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': 'NONE', 'state': 'NONE', 'records_for': 'Account', 'id': nan, 'User_id': nan, 'Legal_Name_of_Business': nan, 'State_Jurisdiction': nan, 'Date_of_Registration': nan, 'Constitution_of_Business': nan, 'Taxpayer_type': nan, 'Nature_of_Business_Activity': nan, 'GSTN_status': nan, 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': nan, 'Trade_Name': nan, 'Additional_place_of_business_address': nan, 'Street': nan, 'Location': nan, 'state_name': nan, 'floor_nbr': nan, 'pin_code': nan, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': nan, 'Pin_Code_repeat': nan, 'created_at': NaT, 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    9 {'user_id': 27, 'gst_number': '08ABECS5596D1Z1', 'username': '9887711126', 'email': 'team@seventhsq.com', 'email_verification_code': 83009, 'gst_in': True, 'company_name': 'Seventh Square Internet Pvt. Ltd.', 'company_verification_type': 'CIN', 'company_verification_number': 'U74999RJ2020PTC071282', 'password_text': '1234', 'password': 'pbkdf2_sha256$260000$b49ljalL8o00fwXqr47PeT$H74Os+sT/ngf2SlYM7Y+LcZvEznpws9+xqUdekFW2aQ=', 'last_login': Timestamp('2024-01-25 04:56:08.363000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-11-01 04:34:22'), 'mobile_number': 9887711126.0, 'is_mobile_number_verified': True, 'receive_order_whatsapp': True, 'receive_order_call': True, 'receive_order_email': True, 'receive_payment_whatsapp': True, 'receive_payment_call': True, 'receive_payment_email': True, 'company_verification': True, 'is_email_verified': False, 'bank_details_done': True, 'gst_details_done': True, 'general_check': True, 'order_handling_time': 0.0, 'order_cutoff_time': '17:00', 'city': 'Jaipur', 'state': 'Rajasthan', 'records_for': 'GST_API_User_data', 'id': 27.0, 'User_id': 27.0, 'Legal_Name_of_Business': 'SEVENTH SQUARE INTERNET PRIVATE LIMITED', 'State_Jurisdiction': 'Circle-C, Jaipur IV, - Ward-I', 'Date_of_Registration': '11/10/2020', 'Constitution_of_Business': 'Private Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Supplier of Services', 'Wholesale Business', 'Retail Business']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'RJ839', 'Trade_Name': 'SEVENTH SQUARE INTERNET PRIVATE LIMITED', 'Additional_place_of_business_address': nan, 'Street': 'JHOTWARA', 'Location': 'JAIPUR', 'state_name': 'Rajasthan', 'floor_nbr': nan, 'pin_code': 302012.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': 'INDUSTRIAL AREA', 'State_name_repeat': 'Rajasthan', 'Pin_Code_repeat': 302012.0, 'created_at': Timestamp('2023-11-01 04:35:43.757000'), 'Data Type': 'Address Data', 'account': 27.0, 'address': '75, Jhotwara Industrial Area', 'pincode': 302012.0, 'latitude': nan, 'longitude': nan, 'isAddressVerified': 0.0, 'addressType': 'COMPANY', 'accountHolderName': 'Aditya Agarwal', 'accountNumber': 919887711126.0, 'ifsc': 'PYTM0123456', 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': 'NO', 'date': Timestamp('2023-12-13 09:10:28.976000'), 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    10 {'user_id': 32, 'gst_number': '27ABPFM6199J1ZC', 'username': '9004910416', 'email': 'info@vizid.in', 'email_verification_code': 60476, 'gst_in': True, 'company_name': 'MKV Technologies LLP', 'company_verification_type': 'CIN', 'company_verification_number': nan, 'password_text': 'Vizid@123', 'password': 'pbkdf2_sha256$260000$NCW13e3CRYCRTheHhx3rc7$lA64WzpbarQUf5n33yhoC6JWEEvxJBaym3CpiG0y2vE=', 'last_login': Timestamp('2024-01-10 05:28:54.562000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-11-22 06:39:35.992000'), 'mobile_number': 9004910416.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': True, 'receive_order_call': True, 'receive_order_email': True, 'receive_payment_whatsapp': True, 'receive_payment_call': True, 'receive_payment_email': True, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': 'Mumbai', 'state': 'Maharashtra', 'records_for': 'GST_API_User_data', 'id': 32.0, 'User_id': 32.0, 'Legal_Name_of_Business': 'MKV Technologies LLP', 'State_Jurisdiction': 'ANDHERI-WEST_701', 'Date_of_Registration': '10/02/2021', 'Constitution_of_Business': 'Limited Liability Partnership', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Others', 'Office / Sale Office', 'Warehouse / Depot']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'MHCG0163', 'Trade_Name': 'MKV Technologies LLP', 'Additional_place_of_business_address': nan, 'Street': 'New Link Road', 'Location': 'Andheri West', 'state_name': 'Maharashtra', 'floor_nbr': nan, 'pin_code': 400053.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': 'D wing Crystal Plaza', 'State_name_repeat': 'Maharashtra', 'Pin_Code_repeat': 400053.0, 'created_at': Timestamp('2023-11-22 06:41:00.874000'), 'Data Type': 'Address Data', 'account': 32.0, 'address': 'B Wing 501, Venus Tower, near Courtyard Family Restaurant', 'pincode': 400053.0, 'latitude': nan, 'longitude': nan, 'isAddressVerified': 0.0, 'addressType': 'COMPANY', 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    11 {'user_id': 22, 'gst_number': '29AAMCA7504L1Z8', 'username': '9831509572', 'email': 'online@waterscience.in', 'email_verification_code': 95286, 'gst_in': True, 'company_name': 'AQUAGENICS RESEARCH AND DEVELOPMENT INDIA PRIVATE LIMITED', 'company_verification_type': 'PAN', 'company_verification_number': 'AAMCA7504L', 'password_text': 'WS2023@A21', 'password': 'pbkdf2_sha256$260000$ncrw2SVIfTpZVnhCuyiOce$7U3iz7llzXDNe1N3wf9bcaVgBCgTi6XOxRcJYlHll/0=', 'last_login': Timestamp('2023-10-25 14:14:41.163000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-10-25 10:17:47.271000'), 'mobile_number': 9831509572.0, 'is_mobile_number_verified': True, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': True, 'is_email_verified': False, 'bank_details_done': True, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': 'Bengaluru', 'state': 'Karnataka', 'records_for': 'GST_API_User_data', 'id': 22.0, 'User_id': 22.0, 'Legal_Name_of_Business': 'AQUAGENICS RESEARCH & DEVELOPMENT INDIA PRIVATE LIMITED', 'State_Jurisdiction': 'LGSTO 036 - Bengaluru', 'Date_of_Registration': '01/07/2017', 'Constitution_of_Business': 'Private Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Office / Sale Office', 'Works Contract', 'Wholesale Business', 'Retail Business', 'Warehouse / Depot', 'Others']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'KA119', 'Trade_Name': 'AQUAGENICS RESEARCH & DEVELOPMENT INDIA PRIVATE LIMITED', 'Additional_place_of_business_address': nan, 'Street': 'Bangalore', 'Location': 'Bengaluru', 'state_name': 'Karnataka', 'floor_nbr': nan, 'pin_code': 560048.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': 'NGEF Ancillary Industrial Estate, Mahadevapura', 'State_name_repeat': 'Karnataka', 'Pin_Code_repeat': 560048.0, 'created_at': Timestamp('2023-10-25 10:18:30.545000'), 'Data Type': 'Address Data', 'account': 22.0, 'address': 'A31, NGEF Estate, Whitefield Main Rd, Mahadevapura, Bengaluru, Karnataka ', 'pincode': 560048.0, 'latitude': nan, 'longitude': nan, 'isAddressVerified': 0.0, 'addressType': 'COMPANY', 'accountHolderName': nan, 'accountNumber': 38164890482.0, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': '257368084149030584846758006128938703144', 'isVerified': 'YES', 'date': Timestamp('2023-10-25 10:48:12.284000'), 'mobile': nan, 'utr': '329816235078', 'name_at_bank': 'AQUAGENICS RESEARCH AND DEVELOPMENT INDI A PRIVATE LIMITED', 'message': 'Bank Account details verified successfully.', 'amount_deposited': 1.0}
    12 {'user_id': 67, 'gst_number': '33AAACM4154G1ZU', 'username': '9567077637', 'email': 'sreerangk77@gmail.com', 'email_verification_code': 76314, 'gst_in': True, 'company_name': 'test', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': '123456', 'password': 'pbkdf2_sha256$260000$QZeFzsX6JqDZjFulRf3R5M$c1nsjdK0MO8eFnwTkp/7wITCAr0R7WpFHfPsKq4Lnbg=', 'last_login': Timestamp('2023-12-02 03:48:42.851000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-11-28 10:37:08.267000'), 'mobile_number': 9567077637.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': ' GOA ', 'state': 'GOA', 'records_for': 'GST_API_User_data', 'id': 62.0, 'User_id': 67.0, 'Legal_Name_of_Business': 'MRF LIMITED', 'State_Jurisdiction': 'EGMORE', 'Date_of_Registration': '01/07/2017', 'Constitution_of_Business': 'Public Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Office / Sale Office', 'Factory / Manufacturing', 'Import', 'Warehouse / Depot', 'Supplier of Services', 'Recipient of Goods or Services', 'Wholesale Business', 'Export', 'Retail Business', 'Bonded Warehouse', 'Leasing Business', 'Others']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'TN057', 'Trade_Name': 'MRF LIMITED', 'Additional_place_of_business_address': nan, 'Street': 'Arkonam Tirutani Road', 'Location': 'Arkonam', 'state_name': 'Tamil Nadu', 'floor_nbr': nan, 'pin_code': 631003.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': 'ICHIPUTHUR', 'State_name_repeat': 'Tamil Nadu', 'Pin_Code_repeat': 631003.0, 'created_at': Timestamp('2023-11-28 10:37:47.766000'), 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    13 {'user_id': 29, 'gst_number': '09AAKCP4075F1Z6', 'username': '9717566244', 'email': 'azrudinmd@pearlproducts.in', 'email_verification_code': 6764, 'gst_in': True, 'company_name': 'Pearl Precision Products Pvt. Ltd.', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': 'Prohome@2023', 'password': 'pbkdf2_sha256$260000$T7QBo3akXpTg19duWFCr6N$wtxhdGZLigko36APp/O3FcNR/fxhE5DfAw87aTjbSIk=', 'last_login': Timestamp('2024-01-18 09:34:52.661000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-11-01 11:22:09.816000'), 'mobile_number': 9717566244.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': True, 'receive_order_call': False, 'receive_order_email': True, 'receive_payment_whatsapp': True, 'receive_payment_call': False, 'receive_payment_email': True, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': 1.0, 'order_cutoff_time': '14:00', 'city': ' GAUTAM BUDDHA NAGAR ', 'state': 'UTTAR PRADESH', 'records_for': 'GST_API_User_data', 'id': 24.0, 'User_id': 29.0, 'Legal_Name_of_Business': 'PEARL PRECISION PRODUCTS PRIVATE LIMITED', 'State_Jurisdiction': 'Noida Sector-14', 'Date_of_Registration': '08/03/2019', 'Constitution_of_Business': 'Private Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Factory / Manufacturing', 'Office / Sale Office', 'Recipient of Goods or Services', 'Import', 'Export', 'Warehouse / Depot', 'Retail Business', 'Wholesale Business']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'UP1591', 'Trade_Name': 'PEARL PRECISION PRODUCTS PRIVATE LIMITED', 'Additional_place_of_business_address': nan, 'Street': 'SECTOR - 81', 'Location': 'NOIDA', 'state_name': 'Uttar Pradesh', 'floor_nbr': nan, 'pin_code': 201305.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': 'Uttar Pradesh', 'Pin_Code_repeat': 201305.0, 'created_at': Timestamp('2023-11-01 11:22:38.788000'), 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    14 {'user_id': 17, 'gst_number': '07AAACO2237Q1Z6', 'username': '9910222333', 'email': 'info@ornatesolar.com', 'email_verification_code': 84969, 'gst_in': True, 'company_name': 'Ornate Agencies Pvt. Limited', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': 'Incredible@@2030', 'password': 'pbkdf2_sha256$260000$jwUp3JywfDOpVXZy5JgMzY$H90ds4X4/kqslS8kpCx6WEl0XijqDHQ/rQILvpelMbE=', 'last_login': Timestamp('2023-10-10 09:54:21.654000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-10-10 09:54:21.461000'), 'mobile_number': 9910222333.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': ' DELHI ', 'state': 'DELHI', 'records_for': 'GST_API_User_data', 'id': 13.0, 'User_id': 17.0, 'Legal_Name_of_Business': 'ORNATE AGENCIES PRIVATE LIMITED', 'State_Jurisdiction': 'Ward 2', 'Date_of_Registration': '01/07/2017', 'Constitution_of_Business': 'Private Limited Company', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Office / Sale Office', 'Recipient of Goods or Services', 'Service Provision']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'DL002', 'Trade_Name': 'ORNATE AGENCIES PRIVATE LIMITED', 'Additional_place_of_business_address': nan, 'Street': 'Barakhamba Road', 'Location': 'New Delhi', 'state_name': 'Delhi', 'floor_nbr': 'Ground Floor', 'pin_code': 110001.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': 'Arunachal Building', 'State_name_repeat': 'Delhi', 'Pin_Code_repeat': 110001.0, 'created_at': Timestamp('2023-10-10 09:59:12.444000'), 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    15 {'user_id': 69, 'gst_number': nan,               'username': '8234097415', 'email': 'ravipatel4075@gmail.com', 'email_verification_code': 9636, 'gst_in': False, 'company_name': nan, 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': '12345', 'password': 'pbkdf2_sha256$260000$PCHbdvAPEXGgVtnTnpaGmy$OTC56RuuyS7awlkCyAhIFyzHX7HwJojjXIbvPPIYTXY=', 'last_login': Timestamp('2023-12-14 06:16:58.353000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-12-14 06:16:58.220000'), 'mobile_number': 8234097415.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': False, 'general_check': False, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': 'NONE', 'state': 'NONE', 'records_for': 'Account', 'id': nan, 'User_id': nan, 'Legal_Name_of_Business': nan, 'State_Jurisdiction': nan, 'Date_of_Registration': nan, 'Constitution_of_Business': nan, 'Taxpayer_type': nan, 'Nature_of_Business_Activity': nan, 'GSTN_status': nan, 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': nan, 'Trade_Name': nan, 'Additional_place_of_business_address': nan, 'Street': nan, 'Location': nan, 'state_name': nan, 'floor_nbr': nan, 'pin_code': nan, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': nan, 'Pin_Code_repeat': nan, 'created_at': NaT, 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    16 {'user_id': 30, 'gst_number': '20AVLPM0318B2ZB', 'username': '9955599070', 'email': 'emaibalajienterprises@gmail.com', 'email_verification_code': 39777, 'gst_in': True, 'company_name': 'Balaji Enterprises', 'company_verification_type': 'PAN', 'company_verification_number': 'AVLPM0318B', 'password_text': 'Sumit@123', 'password': 'pbkdf2_sha256$260000$cFDnM94Scxys9WRQcc546h$v6kQhfgwPMjAmG9XIQYEOcvYUmMrOxlZNr8dK6SQca4=', 'last_login': Timestamp('2024-01-04 18:34:40.011000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-11-09 09:15:24'), 'mobile_number': 9955599070.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': True, 'receive_order_call': False, 'receive_order_email': True, 'receive_payment_whatsapp': True, 'receive_payment_call': False, 'receive_payment_email': True, 'company_verification': True, 'is_email_verified': False, 'bank_details_done': True, 'gst_details_done': True, 'general_check': True, 'order_handling_time': 2.0, 'order_cutoff_time': '08:00', 'city': 'Ranchi', 'state': 'Jharkhand', 'records_for': 'GST_API_User_data', 'id': 30.0, 'User_id': 30.0, 'Legal_Name_of_Business': 'Sumit Kumar Mahalka', 'State_Jurisdiction': 'Ranchi Special', 'Date_of_Registration': '02/07/2017', 'Constitution_of_Business': 'Proprietorship', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Retail Business', 'Supplier of Services', 'Wholesale Business', 'Warehouse / Depot']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'JH025', 'Trade_Name': 'Balaji Enterprises', 'Additional_place_of_business_address': nan, 'Street': 'Behind Durga Mandir', 'Location': 'Ratu', 'state_name': 'Jharkhand', 'floor_nbr': nan, 'pin_code': 834001.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': 'Shahdeo Enclave', 'State_name_repeat': 'Jharkhand', 'Pin_Code_repeat': 834001.0, 'created_at': Timestamp('2023-11-09 09:15:43.209000'), 'Data Type': 'Address Data', 'account': 30.0, 'address': 'Shop No. 8 Sahadeo Enclave Behind Durga Mandir Ratu Road', 'pincode': 834001.0, 'latitude': nan, 'longitude': nan, 'isAddressVerified': 0.0, 'addressType': 'COMPANY', 'accountHolderName': 'Balaji enterprises', 'accountNumber': 1523651100003988.0, 'ifsc': 'IBKL0001523', 'bank': 'IDFC FIRST Bank Limited', 'branch': 'jharkhand', 'beneficiaryID': nan, 'isVerified': 'YES', 'date': Timestamp('2023-12-18 07:06:19'), 'mobile': 9955599070.0, 'utr': 'R7310682908954385', 'name_at_bank': 'IDBI bank', 'message': 'transacation', 'amount_deposited': 1.0}
    17 {'user_id': 20, 'gst_number': '32AACFW6661P1ZN', 'username': '9895398771', 'email': 'rachel@westwoodfloorings.com', 'email_verification_code': 3414, 'gst_in': True, 'company_name': 'Westwood Floorings LLP', 'company_verification_type': 'PAN', 'company_verification_number': 'AACFW6661P', 'password_text': 'Traffichd', 'password': 'pbkdf2_sha256$260000$OwXhl3gtyk3hDJJlQBjtwU$n3lEqoNZ/6zweYx69afy4KkwIuIRYUamLfjCZwnvclQ=', 'last_login': Timestamp('2024-01-13 04:30:34.693000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-10-16 04:41:07.566000'), 'mobile_number': 9895398771.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': True, 'receive_order_call': False, 'receive_order_email': True, 'receive_payment_whatsapp': True, 'receive_payment_call': False, 'receive_payment_email': True, 'company_verification': True, 'is_email_verified': False, 'bank_details_done': True, 'gst_details_done': True, 'general_check': True, 'order_handling_time': 1.0, 'order_cutoff_time': '14:30', 'city': 'kochi', 'state': 'Kerala', 'records_for': 'GST_API_User_data', 'id': 20.0, 'User_id': 20.0, 'Legal_Name_of_Business': 'WESTWOOD FLOORINGS LLP', 'State_Jurisdiction': 'Taxpayer Services  Circle, Thrippunithura', 'Date_of_Registration': '20/10/2017', 'Constitution_of_Business': 'Limited Liability Partnership', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Office / Sale Office']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'KLC288', 'Trade_Name': 'WESTWOOD FLOORINGS LLP', 'Additional_place_of_business_address': nan, 'Street': 'Poornathreyesa Road', 'Location': 'Poonithura, Cochin', 'state_name': 'Kerala', 'floor_nbr': nan, 'pin_code': 682038.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': 'Westwood Heights', 'State_name_repeat': 'Kerala', 'Pin_Code_repeat': 682038.0, 'created_at': Timestamp('2023-10-16 04:47:32.871000'), 'Data Type': 'Address Data', 'account': 20.0, 'address': 'Westwood Heights, Sreepoornathreyesa Road, Gandhi Square, Poonithura, Cochin', 'pincode': 682038.0, 'latitude': nan, 'longitude': nan, 'isAddressVerified': 0.0, 'addressType': 'COMPANY', 'accountHolderName': 'WESTWOOD FLOORINGS LLP', 'accountNumber': 50200027160273.0, 'ifsc': 'HDFC0002835', 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': 'NO', 'date': Timestamp('2023-10-16 05:28:03.439000'), 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    18 {'user_id': 70, 'gst_number': '09AAVFB7148K1ZO', 'username': '9999044170', 'email': 'paridhi@biut.in', 'email_verification_code': 75172, 'gst_in': True, 'company_name': 'Biut Bath Industry', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': 'Paridhi28@', 'password': 'pbkdf2_sha256$260000$otcdPG5o8Px98Hr5Dc92JJ$/OX0FCxgkWAKjzusMqMiidR2L3QW9MQpu14/B5oT4gc=', 'last_login': Timestamp('2023-12-20 13:33:13.273000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-12-20 13:33:13.141000'), 'mobile_number': 9999044170.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': ' GHAZIABAD ', 'state': 'UTTAR PRADESH', 'records_for': 'GST_API_User_data', 'id': 65.0, 'User_id': 70.0, 'Legal_Name_of_Business': 'BIUT BATH INDUSTRY LLP', 'State_Jurisdiction': 'Ghaziabad Sector-15', 'Date_of_Registration': '29/01/2020', 'Constitution_of_Business': 'Limited Liability Partnership', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Retail Business', 'Wholesale Business', 'Factory / Manufacturing']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'UP1623', 'Trade_Name': 'BIUT BATH INDUSTRY LLP', 'Additional_place_of_business_address': nan, 'Street': 'SITE-4', 'Location': 'SAHIBABAD', 'state_name': 'Uttar Pradesh', 'floor_nbr': nan, 'pin_code': 201010.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': 'Uttar Pradesh', 'Pin_Code_repeat': 201010.0, 'created_at': Timestamp('2023-12-20 13:34:02.530000'), 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}


    18 {'user_id': 70, 'gst_number': '09AAVFB7148K1ZO', 'username': '9999044170', 'email': 'paridhi@biut.in', 'email_verification_code': 75172, 'gst_in': True, 'company_name': 'Biut Bath Industry', 'company_verification_type': nan, 'company_verification_number': nan, 'password_text': 'Paridhi28@', 'password': 'pbkdf2_sha256$260000$otcdPG5o8Px98Hr5Dc92JJ$/OX0FCxgkWAKjzusMqMiidR2L3QW9MQpu14/B5oT4gc=', 'last_login': Timestamp('2023-12-20 13:33:13.273000'), 'is_superuser': False, 'is_active': True, 'is_staff': False, 'date_joined': Timestamp('2023-12-20 13:33:13.141000'), 'mobile_number': 9999044170.0, 'is_mobile_number_verified': False, 'receive_order_whatsapp': False, 'receive_order_call': False, 'receive_order_email': False, 'receive_payment_whatsapp': False, 'receive_payment_call': False, 'receive_payment_email': False, 'company_verification': False, 'is_email_verified': False, 'bank_details_done': False, 'gst_details_done': True, 'general_check': True, 'order_handling_time': nan, 'order_cutoff_time': nan, 'city': ' GHAZIABAD ', 'state': 'UTTAR PRADESH', 'records_for': 'GST_API_User_data', 'id': 65.0, 'User_id': 70.0, 'Legal_Name_of_Business': 'BIUT BATH INDUSTRY LLP', 'State_Jurisdiction': 'Ghaziabad Sector-15', 'Date_of_Registration': '29/01/2020', 'Constitution_of_Business': 'Limited Liability Partnership', 'Taxpayer_type': 'Regular', 'Nature_of_Business_Activity': "['Retail Business', 'Wholesale Business', 'Factory / Manufacturing']", 'GSTN_status': 'Active', 'Last_Updated_Date': nan, 'State_Jurisdiction_Code': 'UP1623', 'Trade_Name': 'BIUT BATH INDUSTRY LLP', 'Additional_place_of_business_address': nan, 'Street': 'SITE-4', 'Location': 'SAHIBABAD', 'state_name': 'Uttar Pradesh', 'floor_nbr': nan, 'pin_code': 201010.0, 'Pricipal_Place_of_Business_Address': nan, 'Building_Name': nan, 'State_name_repeat': 'Uttar Pradesh', 'Pin_Code_repeat': 201010.0, 'created_at': Timestamp('2023-12-20 13:34:02.530000'), 'Data Type': nan, 'account': nan, 'address': nan, 'pincode': nan, 'latitude': nan, 'longitude': nan, 'isAddressVerified': nan, 'addressType': nan, 'accountHolderName': nan, 'accountNumber': nan, 'ifsc': nan, 'bank': nan, 'branch': nan, 'beneficiaryID': nan, 'isVerified': nan, 'date': NaT, 'mobile': nan, 'utr': nan, 'name_at_bank': nan, 'message': nan, 'amount_deposited': nan}
    
    '''
    user = request.user

    if user.is_superuser:
        base_url = settings.BASE_DIR
        file_location = f'{base_url}'+'/static/seventh-square/assets/xlsx/one_to_one_field.xlsx'
        # print('base_url-->',file_location)
        df = pd.read_excel(file_location)
        df['accountNumber'] = df['accountNumber'].apply(lambda x: f'{x:.0f}' if not pd.isna(x) else '')
        df_dict = df.to_dict(orient='index')
        # print(df_dict)

        for key, value in df_dict.items():
            user_obj, created = User.objects.get_or_create(
                username=value['email'],
                defaults={
                    'email': value['email'],
                    'is_staff': value['is_staff'],
                    'is_superuser': value['is_superuser'],
                    'is_active': value['is_active'],
                    'date_joined': value['date_joined'],
                    'show_password': value['password_text'],
                    'password': value['password'],
                    'email_verified': value['is_email_verified'],
                }
            )

            if not created:
                user_obj.last_login = value['last_login']
                user_obj.save()



            # GstDetail

            # status, msg = gst_excel_verification_step(value['gst_number'], user_obj)
            '''
                GST saving --> True Pending Gst Verification hritikgoyal19@gmail.com
                GST saving --> False Invalid requesrt. status code found 200 Not Fonund singhabhi.281988@gmail.com
                GST saving --> True Pending Gst Verification aman123kalra@gmail.com
                GST saving --> True Pending Gst Verification ravichovatiya120@gmail.com
                GST saving --> True Pending Gst Verification aditya@gmail.com
                GST saving --> True Pending Gst Verification mamtarani@linklocks.com
                GST saving --> True Pending Gst Verification ecom@foruselectric.com
                GST saving --> True Pending Gst Verification ravichovatiya121@gmail.com
                GST saving --> False Invalid requesrt. status code found 200 Not Fonund jishika0601@gmail.com
                GST saving --> True Pending Gst Verification team@seventhsq.com
                GST saving --> True Pending Gst Verification info@vizid.in
                GST saving --> True Pending Gst Verification online@waterscience.in
                GST saving --> True Pending Gst Verification sreerangk77@gmail.com
                GST saving --> True Pending Gst Verification azrudinmd@pearlproducts.in
                GST saving --> True Pending Gst Verification info@ornatesolar.com
                GST saving --> False Invalid requesrt. status code found 200 Not Fonund ravipatel4075@gmail.com
                GST saving --> True Pending Gst Verification emaibalajienterprises@gmail.com
                GST saving --> True Pending Gst Verification rachel@westwoodfloorings.com
                GST saving --> True Pending Gst Verification paridhi@biut.in

            '''
            # print('GST saving -->',status, msg, user_obj.email)


            # CompanyBasicDetail

            # try:
            #     if value['company_name']:
            #         CompanyBasicDetail.objects.get_or_create(seller=user_obj,
            #             company_name =value['company_name'], defaults={})
            #     else:
            #         print('Not Provided  CompanyBasicDetail:',user_obj.email)

            # except Exception as e:
            #     print('Error for  CompanyBasicDetail:',e,user_obj.email)



            # Company verification 

            # try:
            #     if value['company_verification_type']:
            #         if value['company_verification_type'] == 'PAN' and value['company_verification_number']:
            #             status, msg = pan_excel_verification_step(value['company_verification_number'],user_obj)
            #         else:
            #             status, msg = cin_excel_verification_step(value['company_verification_number'],user_obj)
            #     else:
            #         print("the value is none==>",user_obj.email)

            # except Exception as e:
            #     print('Error for  CompanyBasicDetail:',e,user_obj.email)


            # Bank verification

            # try:
            #     if value['accountHolderName'] and str(value['accountNumber']) and value['ifsc']:
            #         status, msg = bank_excel_details_verification(value['accountHolderName'],value['accountNumber'],value['ifsc'],user_obj)
            #         print("===holdername==>",value['accountHolderName'])
            #         print("===accountNumber==>", str(value['accountNumber']))
            #         print("===ifsc==>",value['ifsc'])

            #         print('bank detail ---->',status, msg, user_obj.email)
            #     else:
            #         print("=======>>>bank all detail are not provide ")

            # except Exception as e:
            #     print('Error for  bankdetail===>>>:',e,user_obj.email)

            # UserPhoneVerified  

            # try:
            #     if int(value['username']):
            #         UserPhoneVerified.objects.get_or_create(seller=user_obj,ph_number=value['username'],
            #             defaults={'is_verified':UserStatusEnums.VERIFIED.value} )
            # except Exception as e:
            #     print("---error phone number-->>>",e, user_obj.email)


            # ProfileSettings
            
            # try:
            #     ProfileSettings.objects.get_or_create(seller=user_obj, defaults={
            #         'receive_order_update_whatsapp':value['receive_order_whatsapp'],
            #         'receive_order_update_call':value['receive_order_call'],
            #         'receive_order_update_email':value['receive_order_email'],
            #         'receive_payment_update_whatsapp':value['receive_payment_whatsapp'],
            #         'receive_payment_update_call':value['receive_payment_call'],
            #         'receive_payment_update_email':value['receive_payment_email']
            #     })
            # except Exception as e:
            #     print("---error phone number-->>>",e, user_obj.email)



            # RepresentativeDetail

            # try:
            #     RepresentativeDetail.objects.get_or_create(seller=user_obj, defaults={
            #         'representative_name':value['representative_name']
            #     })
            # except Exception as e:
            #     print("---Error RepresentativeDetail-->>>",e, user_obj.email)


            # CompanyAddressDetail

            # try:
            #     city_name = value['city']
            #     state_name = value['state']
            #     city_obj = Cities.objects.get(name__iexact=city_name, state__name__iexact = state_name)

            # except Cities.DoesNotExist:
            #     print(f"City or state not found in the database: {value.get('city')}, {value.get('state')}")

            # try:
            #     company_detail = CompanyAddressDetail.objects.get_or_create(seller=user_obj, 
            #         address_line_1=value['address'], pin_code = value['pincode'], state=city_obj.state, city=city_obj,
            #         defaults={})

            # except Exception as e:
            #     print("---->>Error RepresentativeDetail-->>>",e, user_obj.email)



        

        return HttpResponse("Excel file has successfully imported")
    return HttpResponse("invalid user or failed to run the script...............................")


    
