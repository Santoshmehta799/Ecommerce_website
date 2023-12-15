import uuid
from django.db import models
from app_user.models import User
from common.models import ModelMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.


class GstDetail(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_gst_detail",
        default=True,null=True,blank=True)
    company_gst_number = models.CharField(max_length=16,unique=True)

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
    inactive_reason = models.CharField(max_length=225,null=True,blank=True)

    def __str__(self):
        return f"{self.user.id} - {self.company_gst_number}"

    class Meta:
        verbose_name = _('Verification - GST Details')
        verbose_name_plural = _('Verification - GST Details')
