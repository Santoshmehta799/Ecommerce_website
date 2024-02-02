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
    list_filter= ['category__name']

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('id', 'seller', 'product_has_variant','is_active', 'product_title', 'slug', 'created_at', 'updated_at')
    search_fields = ['seller__email', 'id']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


@admin.register(models.ProductBelongDetails)
class ProductBelongDetailsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product', 'product_fetch_status', 'product_fetch_json', 'created_at', 'updated_at')
    search_fields = ['seller__email']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product_id', 'seller_id', 'name', 'value', 'price_on_request', 'default_variant', 'created_at', 'updated_at')
    search_fields = ['product__id', 'id']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    # list_filter = ['default_variant']

    def seller_id(self, obj):
        # Assuming 'product' is a ForeignKey or OneToOneField in YourModel pointing to Product model
        return obj.product.seller.id if obj.product and obj.product.seller else ''
    

@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product_variant_id', 'created_at', 'updated_at')
    search_fields = ['product_variant__id', 'product_variant__product__id']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
   
   
@admin.register(models.ServiceRegions)
class ServiceRegionsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product', 'serviced_regions_description', 'state', 'city', 'created_at', 'updated_at')
    search_fields = ['product_variant']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.PriceStructure)
class PriceStructureAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product_variant', 'mrp', 'tax_code', 'hsn_code', 'sale_price', 'created_at', 'updated_at')
    search_fields = ['product_variant__id']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

@admin.register(models.ShippingDetails)
class ShippingDetailsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product_variant', 'product_weight', 'returnable_product', 'created_at', 'updated_at')
    search_fields = ['product_variant__id']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']


