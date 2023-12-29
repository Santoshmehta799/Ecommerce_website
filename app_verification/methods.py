import random
from django.conf import settings
import requests
import logging
import json
from app.settings import SANDBOX_GST_VERIFY_URL
import app_user
from app_user.models import User
from app_verification.models import GstDetail
from datetime import datetime


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


def sendbox_authentication():
    access_token = None
    try:
        url_sandbox =  f"{settings.SANDBOX_AUTH_TOKEN_URL}"
        headers = {
            "Accept": "application/json",
            "x-api-key": f"{settings.SANDBOX_API_KEY}", 
            "x-api-secret": f"{settings.SANDBOX_SECRET_KEY}",
            "x-api-version": "1.0"
        } 

        response1 = requests.request("POST", url_sandbox, headers=headers)
        resp_dict = json.loads(response1.text) 
        # print('resp_dict -->', resp_dict)
        access_token = resp_dict['access_token']
    except:
        print('sandbox credentials not found!')
    return access_token


def gst_verification_step(company_gst_number, request):
    user = request.user
    # print('=====================>>> GST Verification start here if selected')
    status = True
    msg = 'Pending Gst Verification'
    # redirect = '/account/gstindetail/'
    # resp_dict = None

    if status == True and company_gst_number != '':
        access_token = sendbox_authentication()
        # print("===========>>accesstoken==>>",access_token)

        url_gst_sand = f'{SANDBOX_GST_VERIFY_URL}/{company_gst_number}'
        # print("=========>>>>>>>>>>>>>gst-url",url_gst_sand)
        
        try:
            headers = {
                "Accept": "application/json",
                "x-api-key": f"{settings.SANDBOX_API_KEY}",
                "Authorization": access_token,
                "x-api-version": "1.0"
            }
            gst_verification_response = requests.request('GET',url_gst_sand, headers=headers)
            resp_dict = json.loads(gst_verification_response.text)
            # print('resp_dict ----->', resp_dict)
            if resp_dict['code'] == 200:
                data = resp_dict['data']
                try:
                    gst_detail = GstDetail(
                        user=user,
                        company_gst_number=data['gstin'],
                        legal_name_of_business=data['lgnm'] if 'lgnm' in data else None,
                        state_jurisdiction=data['stj'] if 'stj' in data else None,
                        state_jurisdiction_code=data['stjCd']  if 'stjCd' in data else None,
                        constitution_of_business=data['ctb']  if 'ctb' in data else None,
                        taxpayer_type=data['nba'][0] if 'nba' in data else None,  # Assuming 'nba' is a list and you want the first item
                        nature_of_business_activity=', '.join(data['nba']) if 'nba' in data else None,
                        gstn_status=data['sts'] if 'sts' in data else None,
                        last_updated_date=data['lstupdt'] if 'lstupdt' in data else None,
                        trade_name=data['tradeNam'] if 'tradeNam' in data else None,
                        date_of_registration=datetime.strptime(data['rgdt'], '%d/%m/%Y').date() if 'rgdt' in data else None,
                        is_active=True,
                        response_json=resp_dict  # Save the entire response if needed
                    )
                    gst_detail.save()
                except Exception as e:
                    print('Error:', e)

                # print("Check the request status -->", resp_dict)
            else:
                status = False
                msg = "Invalid requesrt. status code found 200 Not Fonund"
                
        except:
            status = False
            msg = "Gst Verification Failed, No response from api.."

    return status, msg

















