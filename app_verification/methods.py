import random
from django.conf import settings
import requests
import logging
import json
from app.settings import SANDBOX_GST_VERIFY_URL
import app_user
from app_user.models import User
from app_verification.models import BankVerification, GstDetail, PanCinDetails, UserPhoneVerified
from datetime import datetime
import uuid

from common.enums import PanCinDetailEnums


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
                        seller=user,
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
                    msg = f'Error: {e}'
                    print('Error:', e)

                # print("Check the request status -->", resp_dict)
            else:
                status = False
                msg = "Invalid requesrt. status code found 200 Not Fonund"
                
        except:
            status = False
            msg = "Gst Verification Failed, No response from api.."

    return status, msg


def update_gst_verification_step(company_gst_number, request):
    user = request.user
    print('enter to gst number to check update')
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
                    gst_detail = GstDetail.objects.get(seller=user,)
                    gst_detail.company_gst_number=data['gstin']
                    gst_detail.legal_name_of_business=data['lgnm'] if 'lgnm' in data else None
                    gst_detail.state_jurisdiction=data['stj'] if 'stj' in data else None
                    gst_detail.state_jurisdiction_code=data['stjCd']  if 'stjCd' in data else None
                    gst_detail.constitution_of_business=data['ctb']  if 'ctb' in data else None
                    gst_detail.taxpayer_type=data['nba'][0] if 'nba' in data else None  # Assuming 'nba' is a list and you want the first item
                    gst_detail.nature_of_business_activity=', '.join(data['nba']) if 'nba' in data else None
                    gst_detail.gstn_status=data['sts'] if 'sts' in data else None
                    gst_detail.last_updated_date=data['lstupdt'] if 'lstupdt' in data else None
                    gst_detail.trade_name=data['tradeNam'] if 'tradeNam' in data else None
                    gst_detail.date_of_registration=datetime.strptime(data['rgdt'], '%d/%m/%Y').date() if 'rgdt' in data else None
                    gst_detail.is_active=True
                    gst_detail.response_json=resp_dict  # Save the entire response if needed
                    gst_detail.save()
                except Exception as e:
                    msg = f'Error: {e}'
                    print('Error:', e)

                # print("Check the request status -->", resp_dict)
            else:
                status = False
                msg = "Invalid requesrt. status code found 200 Not Fonund"
                
        except:
            status = False
            msg = "Gst Verification Failed, No response from api.."

    return status, msg


def pan_verification_step(company_pan_number, request):
    print('PAN Verification start here if selected')
    status = True
    message = 'Pending Pan Verification'
    user = request.user

    if status == True:
        access_token = sendbox_authentication()
        pan=company_pan_number
        consent="Y"
        reason="For KYC of User"

        url_gst_sand = f'{settings.SANDBOX_PAN_VERIFY_URL}/{pan}/verify?consent={consent}&reason={reason}'
        headers = {
            "Accept": "application/json",
            "x-api-key": f"{settings.SANDBOX_API_KEY}",
            "Authorization": access_token,
            "x-api-version": "1.0"
        } 
        response_bank_sand = requests.request("GET", url_gst_sand, headers=headers)
        print(response_bank_sand.text)
        resp_dict = json.loads(response_bank_sand.text) 
        print(resp_dict['code'])
        print(resp_dict)
        sandbox_code =str(resp_dict['code'])

        if (sandbox_code == "200"):
            print('pan verification status  ---->', resp_dict['data']['status'])
            if resp_dict['data']['status'] == 'VALID':
                try:
                    pan_cin_obj = PanCinDetails.objects.get(seller = user)
                    pan_cin_obj.documnet_id = pan
                    pan_cin_obj.response_json = resp_dict
                    pan_cin_obj.document_type=PanCinDetailEnums.PAN
                    pan_cin_obj.is_verified = True
                    pan_cin_obj.save()
                except:
                    pan_cin_obj = PanCinDetails()
                    pan_cin_obj.seller = user
                    pan_cin_obj.documnet_id = pan
                    pan_cin_obj.response_json = resp_dict
                    pan_cin_obj.document_type=PanCinDetailEnums.PAN
                    pan_cin_obj.is_verified = True
                    pan_cin_obj.save()
                status = True
                message = "Details Verified and Saved."

            else:
                status = False
                message = 'Invaid pan Details Provide..'

        else:
            status = False
            message = "Verification Failed Please Re-enter the PAN Number."

    return status, message


def cin_verification_step(company_cin_number, request):
    print('CIN Verification start here if selected')
    status = True
    message = 'Pending CIN Verification'
    user = request.user

    if status == True:
        access_token = sendbox_authentication()
        cin_id=company_cin_number
        consent="Y"
        reason="For KYC of User"
        url_gst_sand = f'{settings.SANDBOX_CIN_VERIFY_URL}/{cin_id}'
        headers = {
            "Accept": "application/json",
            "x-api-key": f"{settings.SANDBOX_API_KEY}", 
            "Authorization": access_token,
            "x-api-version": "1.0"
        } 
        response_bank_sand = requests.request("GET", url_gst_sand, headers=headers)
        # print(response_bank_sand.text)
        resp_dict = json.loads(response_bank_sand.text)
        print(resp_dict, resp_dict['code'])
        
        if resp_dict['code'] == 200:
            try:
                pan_cin_obj = PanCinDetails.objects.get(seller = user)
                pan_cin_obj.documnet_id = cin_id
                pan_cin_obj.response_json = resp_dict
                pan_cin_obj.document_type=PanCinDetailEnums.CIN
                pan_cin_obj.is_verified = True
                pan_cin_obj.save()
            except:
                pan_cin_obj = PanCinDetails.objects.get()
                pan_cin_obj.seller = user
                pan_cin_obj.documnet_id = cin_id
                pan_cin_obj.response_json = resp_dict
                pan_cin_obj.document_type=PanCinDetailEnums.CIN
                pan_cin_obj.is_verified = True
                pan_cin_obj.save()
            
            status = True
            message = " CIN Number Verification Done."
        else:
            status = False
            message = resp_dict['message']
        # sandbox_code = str(resp_dict['code']) if resp_dict else None
    else:
        status = False
        message = "Company Verification Failed Please Re-enter CIN Number."

    return status, message



def bank_details_verification(account_holder_name, account_number, ifsc, request):
    status = True 
    message = 'Pending Bank Verification'
    user = request.user
    try:
        mobile = UserPhoneVerified.objects.get(seller=user).ph_number
    except:
        mobile = None
    
    if mobile:
        if status == True:
            access_token = sendbox_authentication()
            ifsc = ifsc
            account_number=account_number
            name=account_holder_name
            
            url_bank_sand = f'{settings.SANDBOX_BANK_VERIFY_URL}/{ifsc}/accounts/{account_number}/verify?name={name}&mobile={mobile}'
            headers = {
                "Accept": "application/json",
                "x-api-key": f"{settings.SANDBOX_API_KEY}",
                "Authorization": access_token,
                "x-api-version": "1.0"
            } 
            response_bank_sand = requests.request("GET", url_bank_sand, headers=headers)
            print('======response====>>>',response_bank_sand.text)
            try:
                resp_dict = json.loads(response_bank_sand.text) 
                print('------->>>resp_dict--->>',resp_dict)
                if(resp_dict['code'] == 200):
                    account_exists_value = resp_dict['data'].get('account_exists', False)

                    if account_exists_value is not False:
                        print("code 200", resp_dict)
                        
                        try:
                            sandbox_code = str(resp_dict['data']['account_exists'])
                        except KeyError as e:
                            status = False
                            message=f"Account verification error Please re-enter bank details. ({e})"
                        

                        if (sandbox_code == "True"):
                            print("If is running")

                            id=uuid.uuid4().int
                            id = str(id)
                            try:
                                bank_obj = BankVerification.objects.get(seller=user)
                                bank_obj.account_holder = account_holder_name
                                bank_obj.account_number = account_number
                                bank_obj.ifsc = ifsc
                                bank_obj.response_json = resp_dict
                                bank_obj.is_verified = True
                                bank_obj.save()
                            except:
                                bank_obj = BankVerification()
                                bank_obj.seller= user
                                bank_obj.account_holder = account_holder_name
                                bank_obj.account_number = account_number
                                bank_obj.ifsc = ifsc
                                bank_obj.response_json = resp_dict
                                bank_obj.is_verified = True
                                bank_obj.save()

                            status = True
                            message = "Account Added Successfully"
                    else:
                        status = False
                        message=f"{resp_dict['data']['message']}"

                else:
                    status = False
                    message = f"Something went Wrong, {resp_dict['message']}."
            except json.JSONDecodeError as e:
                print("Error decoding response from API:", e)
                status = False
                message = f"Account verification error Please re-enter bank details. ({e})"
            
            print(resp_dict)
            print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqresp_dict")

            print(resp_dict['code'])
        else:
            status = False
            message = "Invalid Credentials.."
    else:
        status = False
        message = "Contact Details not Found.."
            
    return status, message














