from django import forms
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.models import User
from app_user.helper import OTPField
import re

TERMS_CONDITIONS_LABEL = f"""
    I Agree with <a href="javascript:void(0);" class="text-brand" target="_blank">Marketplace Agreement</a> 
    and <a href="javascript:void(0);" class="text-brand" target="_blank">Terms of Use</a> 
"""

class RegisterForm(forms.Form):
    half_2 = []
    half_3 = ['mobile_send_otp', 'email_send_otp',]
    half_4 = []
    half = []
    half_7 = []
    half_8 = []
    half_9 = ['mobile_number',]
    half_10 = []

    field_order = ['mobile_number', 'mobile_send_otp', 'resend_otp', 'mobile_otp',
        'email', 'password', 'terms_and_conditions']

    email = forms.EmailField(
        max_length=60,
        label="Email",
    )

    mobile_number = forms.CharField(
        max_length=10,
        label="Mobile Number",
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Mobile Number',
                'onkeyup': 'PhoneNumberExist(this.value);',
            }
        ),
    )

    mobile_send_otp = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'button',
                'class':'btn btn-secondary text-wrap py-2 mt-1',
                'style':'font-size:9px;', 
                'value': 'SEND OTP',
                'onclick': 'SendOtpToContactNunber(this.value);',
            }
        ),
    )

    mobile_otp = OTPField(
        label="Mobile OTP",
        required=True,
        widget=forms.HiddenInput(
            attrs={
                'placeholder': 'Enter OTP',
                'onkeyup': 'VerifySendedContactNunber(this.value);',
                'maxlength':'6',
            }
        ),
    )

    password = forms.CharField(
        required=True,
        label="Password",
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password'
            }
        ),
    )

    terms_and_conditions = forms.BooleanField(
        label=TERMS_CONDITIONS_LABEL
    )


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            # 'onkeyup': 'EmailExist(this.value);',
            'placeholder': 'Email'
        })

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=60,
        required = True,
        widget= forms.TextInput(attrs={'placeholder':'Email/Contact No.'}),
    )

    password = forms.CharField(
        required = True,
        widget= forms.PasswordInput(attrs={'placeholder':'Password'}),
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
