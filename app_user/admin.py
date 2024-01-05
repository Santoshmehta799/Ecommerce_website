from django.contrib import admin
from app_user import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user_uuid', 'email', 'username','is_active', 'created_at', 'updated_at')
    search_fields = ['email', 'user_uuid',]
    list_filter = ['is_active',] #  'industry', 'country',
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    # fieldsets = [
    #     (None, {'fields': ['profile_pic_preview','profile_pic']}),
    #     ('USER PROFILE', {'fields': ['user','industry', 'birthdate','gender', 'country']}),
    #     ('CONTACT DETAILS', {'fields': ['ph_number','alternate_ph_number']}),
    #     ('EMAIL DETAILS', {'fields': ['alternate_email']}),
    #     ('VARIFY DETAILS', {'fields': ['otp','otp_send','is_verify','expiry_date','created_at','updated_at']}),
    # ]

@admin.register(models.ProfileSettings)
class ProfileSettingsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'seller', 'receive_order_update_whatsapp', 'receive_order_update_call', 'created_at', 'updated_at')
    search_fields = ['seller__email']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

