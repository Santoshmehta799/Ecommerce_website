from django.contrib import admin
from app_context import models

# Register your models here.

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display  = ('id', 'title', 'image', 'author', 'created_at', 'updated_at')
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.FaqMain)
class FaqMainAdmin(admin.ModelAdmin):
    list_display  = ('id', 'question', 'author', 'tage_type', 'created_at', 'updated_at')
    search_fields = ['question']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

