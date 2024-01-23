from django.contrib import admin
from app_context import models

# Register your models here.

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display  = ('id', 'title', 'image', 'author', 'created_at', 'updated_at')
    search_fields = ['seller__email']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

