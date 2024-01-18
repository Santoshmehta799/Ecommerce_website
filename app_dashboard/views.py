from app_dashboard.models import Cities, States
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from app.settings import APP_LOGIN_URL

from app_user.forms.auth import RegisterForm
from app_user.methods.auth import admin_register_methods, login
from app_user.models import User
from django.contrib import messages
from django.db.models import Q
from django.http.response import JsonResponse
from app_verification.models import TempPhoneVerified


def index_page(request):
    success = ""
    error = ""
    
    if request.user.is_authenticated:
        return redirect('app_dashboard:dashboard-page')
    
    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        mobile_otp = request.POST['mobile_otp']

        try:
            temp_phone_verification = TempPhoneVerified.objects.filter(is_verified = True,
                otp=mobile_otp,otp_send=True).get(ph_number=mobile_number)
            if temp_phone_verification:
                if form.is_valid():
                    try:
                        is_user_exit = User.objects.get(email=email)
                    except:
                        is_user_exit = None

                    if not is_user_exit:
                        try:
                            admin_register_methods(request,form)
                            if login(form, request):
                                messages.success(request,'Thanks you for providing basic authentication details. verification Email Send on Your email.')
                                return redirect('app_verification:get-detail')
                            else:
                                messages.success(request,'Registration sucessfully done!')
                                return redirect('app_user:auth-signin')
                        except:
                            error = "Failed to save user Please Contact Administration."
                    else:
                        error = "User with this email already exists."
        except:
            error = "Otp verification Failed."

    context = {
        'error' : error,
        'success' : success,
        'form' :form,
    }
    return render(request, 'seventh-square/index.html', context)

@login_required()
def dashboard_page(request):
    return render(request, 'app_dashboard/dashboard.html')

@login_required()
def load_city(request):
    if request.method == 'POST':
        state_id = request.POST.get('state_id')
        print('$$$$$$$$$$$$$$ ->',state_id)

        html ="<option disabled value="">---Sub City---</option>"
        city_obj = Cities.objects.filter(state_id = state_id)
        print('city_obj ->', city_obj)
        if city_obj:
            for city in city_obj:
                html += f'<option value="{city.id}">{city.name}</option>'
                
            context = {
                "data": html,
                "status" : True,
            }
            return JsonResponse(context) 
        else:
            context = {
                "data": "",
                "status" : False,
            }
            return JsonResponse(context) 


@login_required()
def load_city_list(request):
    if request.method == 'POST':
        state_id = request.POST.get('state_id')
        print('$$$$$$$$$$$$$$ ->',state_id)
        city_id = []
        city_name = []
        city_obj = Cities.objects.filter(state_id = state_id)
        print('city_obj ->', city_obj)
        if city_obj:
            for city in city_obj:
              city_id.append(city.id)
              city_name.append(city.name)
                
            context = {
                "city_id": city_id,
                "city_name": city_name,
                "status" : True,
            }
            return JsonResponse(context) 
        else:
            context = {
                "city_id": city_id,
                "city_name": city_name,
                "status" : False,
            }
            return JsonResponse(context) 


