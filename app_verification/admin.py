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


@admin.register(models.RepresentativeDetail)
class RepresentativeDetailAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'representative_name', 'created_at', 'updated_at')
    search_fields = ['user__email', 'representative_name',]
    list_filter = []
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


@admin.register(models.UserPhoneVerified)
class UserPhoneVerifiedAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'country', 'ph_number', 'is_verified', 'created_at', 'updated_at')
    search_fields = ['user__email', 'ph_number',]
    list_filter = ['is_verified', ]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']



@admin.register(models.TempPhoneVerified)
class TempPhoneVerifiedAdmin(admin.ModelAdmin):
    list_display  = ('id', 'country', 'ph_number', 'is_verified', 'created_at', 'updated_at')
    search_fields = ['ph_number',]
    list_filter = ['is_verified', ]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


@admin.register(models.CompanyBasicDetail)
class CompanyBasicDetailAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'company_name', 'created_at', 'updated_at')
    search_fields = ['user__email','company_name',]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


@admin.register(models.BankVerification)
class BankVerificationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'account_holder','account_number', 'ifsc', 'bank', 'branch','created_at', 'updated_at')
    search_fields = ['user__email','account_number',]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.PanCinDetails)
class PanCinDetailsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'document_type', 'documnet_id', 'is_verified', 'created_at', 'updated_at')
    search_fields = ['user__email','document_type',]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    