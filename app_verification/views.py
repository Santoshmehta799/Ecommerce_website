from django.shortcuts import render, redirect
import requests
from app_verification.forms.verification import GstDetailForms
from app_verification.methods import gst_verification_step
from app_verification.models import CompanyBasicDetail, GstDetail, RepresentativeDetail
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
# Create your views here.


def verification_home(request):
    return HttpResponse("hello , testing!")

@login_required()
def get_detail(request):
    success = ""
    error = ""
    form = GstDetailForms(request.POST or None)

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
    }
    return render(request, 'app_verification/gst_detail.html', context)


def general_detail(request):
    success = ""
    error = ""

    if request.method == 'POST':
        user = request.user
        representative_name = request.POST.get('representative_name')
        company_name = request.POST.get('company_name')

        if user and representative_name and company_name:
            existing_company = CompanyBasicDetail.objects.filter(company_name=company_name).exists()

            if not existing_company:
                representative_detail, representative_created = RepresentativeDetail.objects.get_or_create(user=user, defaults={"representative_name": representative_name})
                if not representative_created:
                    representative_detail.representative_name = representative_name
                    representative_detail.save()

                company_detail, company_created = CompanyBasicDetail.objects.get_or_create(user=user, defaults={"company_name": company_name})
                if not company_created:
                    company_detail.company_name = company_name
                    company_detail.save()

                success = "Representative and company details saved successfully."
                return redirect('app_dashboard:dashboard-page')
            else:
                error = "The company already exists for the user."
        else:
            error = "Error in form submission. Please check the form and try again."

    context = {
        'error': error,
        'success': success,
    }
    return render(request, 'app_verification/general_detail.html', context)


def gst_check(request):
    company_gst_number = request.POST.get('company_gst_number')
    print(company_gst_number)
    company_gst_number_exist = GstDetail.objects.filter(Q(company_gst_number=company_gst_number))
    if len(company_gst_number_exist)< 1:
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)


    

