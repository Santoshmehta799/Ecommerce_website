import random
from django.conf import settings
import requests
import logging
import json

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
        print('resp_dict -->', resp_dict)
        access_token = resp_dict['access_token']
    except:
        print('sandbox credentials not found!')


# def gst_verification_step(company_gst_number, request):
#     print('GST Verification start here if selected')
#     status = True
#     message = 'Pending Gst Verification'
#     redirect = '/account/gstindetail/'
#     resp_dict = None

#     user = request.user
#     if not user:
#         status = False
#         message = 'User is not found ...'

#     account = None
#     if status:    
#         account = Account.objects.get(id = user.id)
#         if not account:
#             status = False
#             message = 'No account credentials found'

#     if status == True and company_gst_number != '':
#         access_token = sendbox_authentication()

#         url_gst_sand = f'{settings.SANDBOX_GST_VERIFY_URL}/{company_gst_number}'
#         headers = {
#             "Accept": "application/json",
#             "x-api-key": f"{settings.SANDBOX_API_KEY}",
#             "Authorization": access_token,
#             "x-api-version": "1.0"
#         } 
#         response_bank_sand = requests.request("GET", url_gst_sand, headers=headers)

#         print("ssssssssssssss",response_bank_sand.text)
#         resp_dict = json.loads(response_bank_sand.text) 
#         print("Check the request status -->", resp_dict)
#         print("resp_dict-------------------------------------")
#         print(resp_dict['code'])

#         # records fatch and get 200 response
#         if resp_dict['code'] == 200:
#             try:
#                 sandbox_msg =str(resp_dict['data']['error_code'])
#                 if(sandbox_msg=="NOGSTIN" or sandbox_msg== "SWEB_9035"):
#                     if(sandbox_msg=="NOGSTIN"):
#                         print("No gst")
#                         status = False
#                         message = "No records found"

#                     if(sandbox_msg=="SWEB_9035"):
#                         print("kkkkkkkkkkkkkkkkkkkkkkkkwrong gst")
#                         status = False
#                         message = "Invalid GSTIN / UID"
#             except Exception as e :
#                 message = e
#                 status = False
#                 print(e)
#                 pass

#             print("rrrrrrrrrrrrrrrrrrrrr",resp_dict['data'])
            
#             account.companyGSTNumber = company_gst_number
#             gst_details, created = GST_API_User_data.objects.get_or_create(User_id=user)
            
#             print("gst_details")
#             print(gst_details)
#             try:
#                 if(resp_dict['data']['lgnm']):
#                     gst_details.Legal_Name_of_Business=resp_dict['data']['lgnm']
#                 if(resp_dict['data']['stj']):
#                     gst_details.State_Jurisdiction=resp_dict['data']['stj']
#                 if(resp_dict['data']['rgdt']):
#                     gst_details.Date_of_Registration=resp_dict['data']['rgdt']
#                 if(resp_dict['data']['ctb']):
#                     gst_details.Constitution_of_Business=resp_dict['data']['ctb']
#                 if(resp_dict['data']['dty']):
#                     gst_details.Taxpayer_type=resp_dict['data']['dty']
#                 if(resp_dict['data']['nba']):
#                     gst_details.Nature_of_Business_Activity=resp_dict['data']['nba']
#                 if(resp_dict['data']['sts']):
#                     gst_details.GSTN_status=resp_dict['data']['sts']
#                 # if(resp_dict['data']['lstupddt']):
#                 #     gst_details[0].Last_Updated_Date=resp_dict['data']['lstupddt']
#                 if(resp_dict['data']['stjCd']):
#                     gst_details.State_Jurisdiction_Code=resp_dict['data']['stjCd']
#                 if(resp_dict['data']['tradeNam']):
#                     gst_details.Trade_Name=resp_dict['data']['tradeNam']
#                 # if(resp_dict['data']['pradr']['addr']):
#                 #     gst_details[0].Additional_place_of_business_address=resp_dict['data']['pradr']['addr']
#                 if(resp_dict['data']['pradr']['addr']['bnm']):
#                     gst_details.Building_Name=resp_dict['data']['pradr']['addr']['bnm']
#                 if(resp_dict['data']['pradr']['addr']['st']):
#                     gst_details.Street=resp_dict['data']['pradr']['addr']['st'] 
#                 if(resp_dict['data']['pradr']['addr']['loc']):
#                     gst_details.Location=resp_dict['data']['pradr']['addr']['loc']
#                 if(resp_dict['data']['pradr']['addr']['stcd']):
#                     gst_details.state_name=resp_dict['data']['pradr']['addr']['stcd']
#                 if(resp_dict['data']['pradr']['addr']['flno']):
#                     gst_details.floor_nbr=resp_dict['data']['pradr']['addr']['flno']
#                 if(resp_dict['data']['pradr']['addr']['pncd']):
#                     gst_details.pin_code = resp_dict['data']['pradr']['addr']['pncd']
#                 if(resp_dict['data']['pradr']['addr']['stcd']):
#                         gst_details.State_name_repeat=resp_dict['data']['pradr']['addr']['stcd']
#                 if(resp_dict['data']['pradr']['addr']['pncd']):
#                     gst_details.Pin_Code_repeat=resp_dict['data']['pradr']['addr']['pncd']

#                 gst_details.save()
#                 status = True
#                 message = "Gst Details Saved Successfully."
#                 redirect = '/account/generaldetail'
#             except Exception as e :
#                 message = e
#                 status = False
#                 print(e)
#                 pass


#             if(account.companyGSTNumber !='' or company_gst_number !=''):      
#                 account.Gstdetails_done=True
#                 account.gstIn=True
#                 account.save()

#                 status = True
#                 message = "Gst Details Saved Successfully."
#                 redirect = '/account/generaldetail'

#         else :
#             status = False
#             reason = resp_dict['message']
#             message = f"Can't process your request. {reason}"

#     print('get verification variables ->', status, message, redirect, resp_dict, company_gst_number)
#     return status, message, redirect, resp_dict

















