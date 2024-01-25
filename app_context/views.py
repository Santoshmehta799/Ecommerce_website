import requests
from django.shortcuts import render
from common.enums import ChoicesTypeEnums, ChoicesBlogTypeEnums
from app_context.models import Blog, FaqMain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app_inventory.models import Category, ProductType
# Create your views here.

def cancellation_return_policy(request):
   return render(request, 'app_context/cancellation_return_policy.html')


def shipping_policy(request):
    return render(request, 'app_context/shipping_policy.html')


def payment_policy(request):
    return render(request, 'app_context/payment_policy.html')


def guidelines(request):
    return render(request, 'app_context/guidelines.html')


def sell_with_us(request):
    return render(request, 'app_context/sell_with_us.html')


def how_it_work(requset):
    return render(requset, 'app_context/how_it_work.html')


def advertise_with_us(request):
    return render(request, 'app_context/advertise_with_us.html')


def pricing_and_commission(request):
    return render(request, 'app_context/pricing_and_commission.html')


def price_calculator(request):
    category = Category.objects.all()
    product_type = ProductType.objects.all()
    return render(request, 'app_context/price_calculator.html', context={"cate":category, "subcat":product_type})


def about_us(request):
    return render(request, 'app_context/about_us.html')


def help_center(request):
    return render(request, 'app_context/help_center.html')


def getting_started(request):
    return render(request, 'app_context/help-center/getting_started.html')

def manage_your_account(request):
    return render(request, 'app_context/help-center/manage_your_account.html')

def adding_products(request):
    return render(request, 'app_context/help-center/adding_products.html')

def processing_orders(request):
    return render(request, 'app_context/help-center/processing_orders.html')

def pricing_payments(request):
    return render(request, 'app_context/help-center/pricing_payments.html')

def shipping_returns(request):
    return render(request, 'app_context/help-center/shipping_returns.html')


# def learning_center(request):
#     return render(request, 'app_context/learning_center.html')


def faq(request):
    gs = request.GET.get('gs')
    mya = request.GET.get('mya')
    ap = request.GET.get('ap')
    po = request.GET.get('po')
    pp = request.GET.get('pp')
    sr = request.GET.get('sr')
    a = request.GET.get('a')
    e = request.GET.get('e')
    dr = request.GET.get('dr')
    ps = request.GET.get('ps')


    if gs:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.GETTING_STARTED).order_by('-created_at')[:10]
    elif mya:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.MANAGE_YOUR_ACCOUNT)
    elif ap:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.ADDING_PRODUCTS)
    elif po:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.PROCESSING_ORDERS)
    elif pp:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.PRICING_PAYMENTS)
    elif sr:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.SHIPPING_RETURNS)
    elif a:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.ADVERTISING)
    elif e:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.ENQUIRIES)
    elif dr:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.DISPUTES_RESOLUTION)
    elif ps:
        posts = FaqMain.objects.filter(tage_type=ChoicesTypeEnums.POLICY_SECURITY)
        
    else:
        posts = FaqMain.objects.all()
    context = {'posts': posts[0:10],}

    return render(request, 'app_context/faq.html', context)


def active_products(request):
    return render(request, 'app_context/active_products.html')


def page_not_found(request):
    return render(request, 'app_context/page_not_found.html')


def learning_center(request):
    blog_objs = Blog.objects.all()
    
    sort = request.GET.get('sort', None)
    order = request.GET.get('order', 'asc')

    if sort == 'asc':
        blog_objs = blog_objs.order_by('title')
    elif sort == 'desc':
        blog_objs = blog_objs.order_by('-title')
    elif sort == 'adp':
        blog_objs = blog_objs.filter(Blog_type=ChoicesBlogTypeEnums.ADD_NEW_PRODUCT)
        if order == 'asc':
            blog_objs = blog_objs.order_by('title')
        elif order == 'desc':
            blog_objs = blog_objs.order_by('-title')
    elif sort == 'pg':
        blog_objs = blog_objs.filter(Blog_type=ChoicesBlogTypeEnums.PLATFORM_GUIDE)
        if order == 'asc':
            blog_objs = blog_objs.order_by('title')
        elif order == 'desc':
            blog_objs = blog_objs.order_by('-title')
    elif sort == 'tt':
        blog_objs = blog_objs.filter(Blog_type=ChoicesBlogTypeEnums.TIPS_AND_TRICKS)
        if order == 'asc':
            blog_objs = blog_objs.order_by('title')
        elif order == 'desc':
            blog_objs = blog_objs.order_by('-title')
    elif sort == 'pu':
        blog_objs = blog_objs.filter(Blog_type=ChoicesBlogTypeEnums.PLATFORM_UPDATES)
        if order == 'asc':
            blog_objs = blog_objs.order_by('title')
        elif order == 'desc':
            blog_objs = blog_objs.order_by('-title')
            
    per_page_records = 6
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blog_objs, per_page_records)
    try:
        blog_objs = paginator.page(page_num)
    except PageNotAnInteger:
        blog_objs = paginator.page(1)
    except EmptyPage:
        blog_objs = paginator.page(paginator.num_pages)
    

    context = {
        "paginator": paginator,
        "blog_objs": blog_objs
        
  
    }
    return render(request, 'app_context/learning_center.html',context)