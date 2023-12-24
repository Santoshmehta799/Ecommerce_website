import random
import requests
import logging

OTP_LENGTH = 6
def generate_otp():
    otp = [str(random.randint(0, 9)) for _ in range(OTP_LENGTH)]
    return ''.join(otp)


def registration_otp_send(contact_number, otp):
    status = False
    api_key = 'd04e6b44-114b-11eb-9fa5-0200cd936042'
    template_name = 'OTP SMS'
    url = f"https://2factor.in/API/V1/{api_key}/SMS/{contact_number}/{otp}/{template_name}"
    send_request = requests.request('GET', url)
    if send_request.status_code==200:
        status = True
    else:
        logger = logging.getLogger(__name__)
        logger.error('twoFactorAuth 40 error')
        status = False
    return status