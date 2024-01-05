import uuid
import os.path
from datetime import datetime
from uuid import uuid4
from os.path import join
from django.db import models
from app_dashboard.models import Cities, States
from app_user.models import User
from common import enums, validators
from common import helpers
from common.models import ModelMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.


class GstDetail(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.OneToOneField(User,on_delete=models.CASCADE,related_name="seller_gst_detail")
    company_gst_number = models.CharField(max_length=15, unique=True,
        validators=[validators.gst_validator])
    legal_name_of_business = models.CharField(max_length=225,null=True,blank=True)
    state_jurisdiction = models.CharField(max_length=225,null=True,blank=True)
    state_jurisdiction_code = models.CharField(max_length=225, null=True, blank=True)
    date_of_registration = models.DateField(null=True,blank=True)
    constitution_of_business = models.CharField(max_length=225,null=True,blank=True)
    taxpayer_type = models.CharField(max_length=225,null=True,blank=True)
    nature_of_business_activity = models.CharField(max_length=700,null=True,blank=True)
    gstn_status = models.CharField(max_length=225, null=True, blank=True)
    last_updated_date = models.CharField(max_length=225, null=True, blank=True)
    trade_name = models.CharField(max_length=700, null=True, blank=True)
    additional_place_of_business_address = models.CharField(max_length=225, null=True, blank=True)
    building_name = models.CharField(max_length=225, null=True, blank=True)
    street = models.CharField(max_length=225, null=True, blank=True)
    location = models.CharField(max_length=225, null=True, blank=True)
    state_name = models.CharField(max_length=225, null=True, blank=True)
    floor_nbr = models.CharField(max_length=225, null=True, blank=True)
    pin_code = models.CharField(max_length=6, null=True, blank=True)
    pricipal_place_of_business_address = models.CharField(max_length=225, null=True, blank=True)
    state_name_repeat = models.CharField(max_length=225, null=True, blank=True)
    pin_code_repeat = models.CharField(max_length=6, null=True, blank=True)
    response_json = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    reject_reason = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return f"{self.seller.id} - {self.company_gst_number}"

    class Meta:
        verbose_name = _('Verification - GST Details')
        verbose_name_plural = _('Verification - GST Details')


class RepresentativeDetail(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.OneToOneField(User,on_delete=models.CASCADE,related_name="seller_representative_detail",)
    representative_name = models.CharField(max_length=100, blank=True, null=True)
    representative_image = models.FileField(
        upload_to=helpers.FileUploadPath('representative_proof'),
        validators=[validators.image_validator],
        help_text="please Uploaded Documents above.",
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.seller.id} - {self.representative_name}"
    class Meta:
        verbose_name = _('Verification - Representative Detail')
        verbose_name_plural = _('Verification - Representative Detail')


class UserPhoneVerified(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.OneToOneField(User, on_delete=models.CASCADE,related_name="seller_phone_number")
    country = models.CharField(
        choices=enums.CountryWithDialCodeEnums.choices,
        max_length=50,
        default=enums.CountryWithDialCodeEnums.IN,
        validators=[validators.country_validator],
    )
    ph_number = models.CharField(max_length=15, validators=[validators.phone_validator])
    otp = models.CharField(max_length=6, default='', blank=True)
    otp_send = models.BooleanField(default=False)
    is_verified = models.CharField(max_length=10,
        choices=enums.UserStatusEnums.choices,
        default=enums.UserStatusEnums.PENDING
    )
    reset_password_verify = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(null=True,blank=True)
    reject_reason = models.TextField(default='', blank=True, null=True)

    class Meta:
        verbose_name = _("Verification - Phone")
        verbose_name_plural = _("Verification - Phone")

    def __str__(self):
        return self.seller.username
    
    
class TempPhoneVerified(ModelMixin):
    '''
        This model is used while registration, this will work
        to verify user mobile number.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(
        choices=enums.CountryWithDialCodeEnums.choices,
        max_length=50,
        default=enums.CountryWithDialCodeEnums.IN,
        validators=[validators.country_validator],
    )
    ph_number = models.CharField(max_length=15, validators=[validators.phone_validator])
    otp = models.CharField(max_length=6, default='', blank=True)
    otp_send = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Verification - Temp Phone Verification")
        verbose_name_plural = _("Verification - Temp Phone Verification")

    def __str__(self):
        return f"{self.ph_number} - {self.otp} - {self.is_verified}"
        

class CompanyBasicDetail(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.OneToOneField(User, on_delete=models.CASCADE,related_name="seller_company_detail")
    company_name = models.CharField(max_length=255, unique=True)
    about_brand = models.CharField(max_length=500, null=True, blank=True)


    class Meta:
        verbose_name = _("Verification - Company Basic Detail")
        verbose_name_plural = _("Verification - Company Basic Detail")

    def __str__(self):
        return f"{self.seller.username} - {self.company_name} "
    

class CompanyAddressDetail(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.OneToOneField(User, on_delete=models.CASCADE,related_name="seller_company_address")
    address_line_1 = models.CharField(max_length=500,blank=True,null=True)
    address_line_2 = models.CharField(max_length=200,blank=True,null=True)
    state = models.ForeignKey(States, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(Cities, on_delete=models.DO_NOTHING)
    pin_code = models.CharField(max_length=6,validators=[validators.pin_validator], 
        null=True, blank=True)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Verification - Company Address Detail")
        verbose_name_plural = _("Verification - Company Address Detail")
    
    def __str__(self):
        return f"{self.seller.username} - {self.address_line_1} "
    

class BankVerification(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.OneToOneField(User, on_delete=models.CASCADE,related_name="seller_bank_verification")
    account_holder = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20,unique=True)
    ifsc = models.CharField(max_length=11)
    bank = models.CharField(max_length=255, null=True, blank=True)
    branch = models.CharField(max_length=225, null=True, blank=True)
    beneficiary_id = models.CharField(max_length=225, null=True, blank=True)
    mobile = models.CharField(max_length=13, default='')
    utr = models.CharField(max_length=50, null=True, blank=True)
    name_at_bank = models.CharField(max_length=100,null=True, blank=True)
    amount_deposited = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=100, null=True, blank=True) 
    is_verified = models.BooleanField(default=False)
    reject_reason = models.TextField(default='', blank=True, null=True)
    response_json = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        verbose_name = _("Verification - Bank Detail")
        verbose_name_plural = _("Verification - Bank Detail")

    def __str__(self):
        return f"{self.account_holder} - {self.account_number}"


class PanCinDetails (ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.OneToOneField(User, on_delete=models.CASCADE,related_name="seller_pan_cin_detail")
    document_type = models.CharField(max_length=5, choices=enums.PanCinDetailEnums.choices, 
        null=True, blank=True)
    documnet_id = models.CharField(max_length=255, unique=True)
    response_json = models.JSONField(default=dict, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    reject_reason = models.TextField(default='', blank=True, null=True)

    class Meta:
        verbose_name = _("Verification - Pan Cin Detail")
        verbose_name_plural = _("Verification - Pan Cin Detail")

    def __str__(self):
        return f"{self.user.username} - {self.document_type}"



