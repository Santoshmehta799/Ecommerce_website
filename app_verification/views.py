from django.shortcuts import render, redirect
import requests
from app_verification.forms.verification import GstDetailForms
from app_verification.methods import gst_verification_step
from app_verification.models import CompanyBasicDetail, GstDetail, RepresentativeDetail
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def verification_home(request):
    return HttpResponse("hello , testing!")

@login_required()
def get_detail(request):
    success = ""
    error = ""
    user = request.user
    gst_detail_obj = None
    try:
        gst_detail_obj = GstDetail.objects.get(user=user)
        if gst_detail_obj.is_active:
            return redirect('app_verification:general-detail')
    except:
        pass

    form = GstDetailForms(request.POST or None, instance=gst_detail_obj)

    if request.method == 'POST':
        if form.is_valid():
            company_gst_number = form.data['company_gst_number']
            if company_gst_number:
                status, msg = gst_verification_step(company_gst_number, request)
                if status == True:
                    return redirect('app_verification:general-detail') 
                else:
                    error = msg
            # print("=============>>",company_gst_number)
            # form_obj = form.save(inplace=True)
            # form_obj.user = request.user
            # form_obj.save()
    
    context = {
        'error' : error,
        'success' : success,
        'form' :form,
        'gst_detail_obj': gst_detail_obj
    }
    return render(request, 'app_verification/gst_detail.html', context)

@login_required()
def general_detail(request):
    success = ""
    error = ""
    user = request.user
    try:
        company_basic_detail = CompanyBasicDetail.objects.get(user=user)
        representative_detail = RepresentativeDetail.objects.get(user=user)
        if company_basic_detail.company_name is not None and \
            representative_detail.representative_name is not None:
            return redirect('app_dashboard:dashboard-page')
    except:
        company_basic_detail = None
        representative_detail = None

    if request.method == 'POST':
        user = request.user
        representative_name = request.POST.get('representative_name')
        company_name = request.POST.get('company_name')

        if representative_name and company_name:
            existing_company = CompanyBasicDetail.objects.filter(company_name=company_name).exists()
            if not existing_company:
                representative_detail, representative_created = RepresentativeDetail.objects.get_or_create(user=user, 
                    defaults={"representative_name": representative_name})
                if not representative_created:
                    representative_detail.representative_name = representative_name
                    representative_detail.save()

                company_detail, company_created = CompanyBasicDetail.objects.get_or_create(user=user, defaults={"company_name": company_name})
                if not company_created:
                    company_detail.company_name = company_name
                    company_detail.save()
                print('enter hear')
                messages.success(request, 'Representative and company details saved successfully.')
                return redirect('app_dashboard:dashboard-page')
            else:
                error = "The company already exists for the user."
        else:
            error = "please add representative_name, company_name. try again."

    context = {
        'error': error,
        'success': success,
    }
    return render(request, 'app_verification/general_detail.html', context)

@login_required()
def gst_check(request):
    company_gst_number = request.POST.get('company_gst_number')
    print(company_gst_number)
    company_gst_number_exist = GstDetail.objects.filter(Q(company_gst_number=company_gst_number))
    if len(company_gst_number_exist)< 1:
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)
    


@login_required
def except_user_gst_check(request):
    if request.method == 'POST':
        company_gst_number = request.POST.get('company_gst_number')
        print(company_gst_number)

        try:
            current_user_gst = GstDetail.objects.get(user=request.user)
        except ObjectDoesNotExist:
            current_user_gst = None

        gst_exist = GstDetail.objects.filter(company_gst_number=company_gst_number).exclude(pk=current_user_gst.pk if current_user_gst else None)

        if len(gst_exist) < 1:
            return JsonResponse(True, safe=False)
        else:
            return JsonResponse(False, safe=False)


    

