


from app import settings
from app_user.models import User
from app_user import tokens
from django.contrib import auth
from app_verification.models import UserPhoneVerified
from common.enums import UserStatusEnums
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import smart_str,force_bytes, DjangoUnicodeDecodeError
from django.utils.html import strip_tags
from django.core.mail import send_mail, BadHeaderError,EmailMultiAlternatives


def send_registration_mail(mail_subject, current_site,template_path, user,):
    try:
        html_content = render_to_string(template_path, {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': tokens.account_activation_token.make_token(user),
                    'username': user.email,
                })
        text_content = strip_tags(html_content)
        to_email = user.email
        email_to_send = EmailMultiAlternatives(mail_subject, text_content,settings.EMAIL_HOST_USER, [to_email])
        email_to_send.attach_alternative(html_content,'text/html')
        email_to_send.send()

        print("msg", email_to_send)
        print("3.1 : mail sended")
        print('user successfully created !')
    
    except Exception as e:
        print("3.2 : error whilw sending mail")
        print('error ->',e)


def admin_register_methods(request,form):
    # fatch form and clean
    password = form.cleaned_data.get('password')
    email = form.cleaned_data.get('email').lower()
    mobile_number = form.cleaned_data.get('mobile_number')
    mobile_otp = form.cleaned_data.get('mobile_otp')

    # creating user
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        show_password=password,
        is_active=True
    )
    print('1. user created')

    user_phone_verified = UserPhoneVerified(
        user_id=user.id,
        ph_number=mobile_number,
        otp_send =True,
        otp=mobile_otp,
        is_verified=UserStatusEnums.VERIFIED.value,
    )
    user_phone_verified.save()

    #Send Registration mail configrations
    mail_subject = 'Activate your account.'
    current_site = get_current_site(request)
    template_path = f'app_user/mail/initial-admin-registration.html'
    user = user
    print('3. before sending the user mail')
    send_registration_mail(mail_subject, current_site, template_path, user)
    print('2. user created')


def login(form, request):
    try:
        user = User.objects.get(email = form.data['email'].lower())
        username = user.username
    except:
        username = form.data['email'].lower()

    user = auth.authenticate(
        username = username,
        password=form.data['password']
    )
    if user is not None:
        auth.login(request, user)
        return True
    else:
        return False
    