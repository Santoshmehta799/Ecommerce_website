from django.contrib import admin
from app_inventory import models

# Register your models here.
@admin.register(models.PickUpWarehouseLocation)
class PickUpWarehouseLocationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'plot_no', 'location_name', 'created_at', 'updated_at')
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']