import requests
from app_context.models import Blog
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    return render(request, 'app_context/price_calculator.html')


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
    return render(request, 'app_context/faq.html')


# def current_orders(request):
#     return render(request, 'app_context/current_orders.html')


def active_products(request):
    return render(request, 'app_context/active_products.html')


# def payment_history(request):
#     return render(request, 'app_context/payment_history.html')

def page_not_found(request):
    return render(request, 'app_context/page_not_found.html')


def learning_center(request):
    blog_objs = Blog.objects.all()
    print("==========>>>",blog_objs)
    
    # sort = request.GET.get('sort', None)
    # order = request.GET.get('order', 'asc')

    # if sort == 'asc':
    #     blog_objs = blog_objs.order_by('title')
    # elif sort == 'desc':
    #     blog_objs = blog_objs.order_by('-title')
    # elif sort == 'adp':
    #     blog_objs = blog_objs.filter(Blog_type='Add new product')
    #     if order == 'asc':
    #         blog_objs = blog_objs.order_by('title')
    #     elif order == 'desc':
    #         blog_objs = blog_objs.order_by('-title')
    # elif sort == 'pg':
    #     blog_objs = blog_objs.filter(Blog_type='Platform Guide')
    #     if order == 'asc':
    #         blog_objs = blog_objs.order_by('title')
    #     elif order == 'desc':
    #         blog_objs = blog_objs.order_by('-title')
    # elif sort == 'tt':
    #     blog_objs = blog_objs.filter(Blog_type='Tips & Tricks')
    #     if order == 'asc':
    #         blog_objs = blog_objs.order_by('title')
    #     elif order == 'desc':
    #         blog_objs = blog_objs.order_by('-title')
    # elif sort == 'pu':
    #     blog_objs = blog_objs.filter(Blog_type='Platform Updates')
    #     if order == 'asc':
    #         blog_objs = blog_objs.order_by('title')
    #     elif order == 'desc':
    #         blog_objs = blog_objs.order_by('-title')
            
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
        # "sort": sort,
        "paginator": paginator,
        "blog_objs": blog_objs
        
  
    }
    return render(request, 'app_context/learning_center.html',context)