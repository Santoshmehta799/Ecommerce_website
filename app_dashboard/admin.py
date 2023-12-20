from django.contrib import admin
from app_dashboard.models import States, Cities, Country

# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["id","name","iso2_code","iso3_code","is_active","created_at","updated_at"]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(States)
class StateAdmin(admin.ModelAdmin):
    list_display = ["id","country","name","state_code","is_active","created_at","updated_at"]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


@admin.register(Cities)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "country", "state","name","pin_code","is_active","created_at","updated_at"]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def country(self,obj):
        return obj.state.country.name
