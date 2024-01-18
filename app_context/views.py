from django.shortcuts import render
import requests
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


def seller_register(request):
    return render(request, 'app_context/seller_register.html')


def help_center(request):
    return render(request, 'app_context/help_center.html')


def learning_center(request):
    return render(request, 'app_context/learning_center.html')


def faq(request):
    return render(request, 'app_context/faq.html')


def profile(request):
    return render(request, 'app_context/profile.html')


def current_orders(request):
    return render(request, 'app_context/current_orders.html')


def active_products(request):
    return render(request, 'app_context/active_products.html')


def customer_enquiry(request):
    return render(request, 'app_context/customer_enquiry.html')

def payment_history(request):
    return render(request, 'app_context/payment_history.html')