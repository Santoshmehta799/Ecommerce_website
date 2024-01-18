from django.urls import path
from app_context import views
from django.views.generic import TemplateView

app_name="app_context"

urlpatterns=[

    # policy
    path('cancellation-return-policy/', views.cancellation_return_policy, name="cancellation-return-policy"),
    path('shipping-policy/', views.shipping_policy, name="shipping-policy"),
    path('payment-policy/', views.payment_policy, name="payment-policy"),
    path('guidelines/', views.guidelines, name="guidelines"),

    # resources
    path('sell-with-us/', views.sell_with_us, name="cancellation-return-policy"),
    path('how-it-work/', views.how_it_work, name="how-it-work"),
    path('advertise-with-us/', views.advertise_with_us, name="advertise-with-us"),
    path('pricing-and-commission/', views.pricing_and_commission, name="pricing-and-commission"),
    path('price-calculator/', views.price_calculator, name="price-calculator"),

    # help
    path('about-us/', views.about_us, name="about-us"),
    path('seller-register/', views.seller_register, name="seller-register"),
    path('help-center/', views.help_center, name="help-center"),
    path('learning-center/', views.learning_center, name="learning-center"),
    path('faq/', views.faq, name="faq"),

    # account
    path('profile/', views.profile, name="profile"),
    path('current-orders/', views.current_orders, name="current-orders"),
    path('active-products/', views.active_products, name="active-products"),
    path('customer-enquiry/', views.customer_enquiry, name="customer-enquiry"),
    path('payment-history/', views.payment_history, name="payment-history"),
]