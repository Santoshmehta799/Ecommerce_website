from django.contrib import admin
from app_inventory import models

# Register your models here.
@admin.register(models.PickUpWarehouseLocation)
class PickUpWarehouseLocationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'seller', 'plot_no', 'location_name', 'created_at', 'updated_at')
    search_fields = ['seller__email']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'slug', 'created_at', 'updated_at')
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display  = ('id', 'category', 'name', 'slug', 'commission_type', 'created_at', 'updated_at')
    search_fields = ['category__name']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('id', 'seller', 'product_title', 'slug', 'created_at', 'updated_at')
    search_fields = ['seller__email']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.ProductBelongDetails)
class ProductBelongDetailsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product', 'product_fetch_status', 'product_fetch_json', 'created_at', 'updated_at')
    search_fields = ['seller__email']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'price_on_request', 'product', 'default_varient', 'created_at', 'updated_at')
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product_variant', 'created_at', 'updated_at')
    search_fields = ['product_variant']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.ServiceRegions)
class ServiceRegionsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product_variant', 'serviced_regions_description', 'state', 'city', 'created_at', 'updated_at')
    search_fields = ['product_variant']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.PriceStructure)
class PriceStructureAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product_variant', 'sale_price', 'minimum_order_qunatity', 'minimum_order_qunatity_unit', 'created_at', 'updated_at')
    search_fields = ['product_variant']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.ShippingDetails)
class ShippingDetailsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product_variant', 'pick_up_location', 'product_weight', 'returnable_product', 'created_at', 'updated_at')
    search_fields = ['product_variant']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


