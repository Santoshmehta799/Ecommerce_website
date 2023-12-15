from django.contrib import admin
from app_dashboard.models import States, Cities

# Register your models here.


@admin.register(States)
class StateAdmin(admin.ModelAdmin):
    list_display = ["id","name","is_active","created_at","updated_at"]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


@admin.register(Cities)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id","state","name","pin_code","is_active","created_at","updated_at"]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
