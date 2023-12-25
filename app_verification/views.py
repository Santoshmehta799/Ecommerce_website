from django.shortcuts import render
from django.http import HttpResponse
from app_verification.forms.verification import GstDetailForms
from app_verification.models import GstDetail
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
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
            form_obj = form.save(inplace=True)
            form_obj.user = request.user
            form_obj.save()
    
    context = {
        'error' : error,
        'success' : success,
        'form' :form,
    }
    return render(request, 'app_verification/gst_detail.html', context)

def general_detail(request):
    return render(request, 'app_verification/general_detail.html')


def gst_check(request):
    company_gst_number = request.POST.get('company_gst_number')
    print(company_gst_number)
    company_gst_number_exist = GstDetail.objects.filter(Q(company_gst_number=company_gst_number))
    if len(company_gst_number_exist)< 1:
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)


    

