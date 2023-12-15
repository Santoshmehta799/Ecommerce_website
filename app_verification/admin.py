from django.contrib import admin
from app_verification import models

# Register your models here.
@admin.register(models.GstDetail)
class GstDetailAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'company_gst_number', 'is_active', 'legal_name_of_business', 'created_at', 'updated_at')
    search_fields = ['email', 'company_gst_number',]
    list_filter = ['is_active',]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    # fieldsets = [
    #     (None, {'fields': ['profile_pic_preview','profile_pic']}),
    #     ('USER PROFILE', {'fields': ['user','industry', 'birthdate','gender', 'country']}),
    #     ('CONTACT DETAILS', {'fields': ['ph_number','alternate_ph_number']}),
    #     ('EMAIL DETAILS', {'fields': ['alternate_email']}),
    #     ('VARIFY DETAILS', {'fields': ['otp','otp_send','is_verify','expiry_date','created_at','updated_at']}),
    # ]