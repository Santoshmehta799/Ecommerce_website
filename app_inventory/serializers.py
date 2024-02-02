from django.db.models import fields
from django.db.models.fields import files
from rest_framework import serializers

from app_inventory.models import Category, Product, ProductType, ProductVariant, \
    ServiceRegions, ProductBelongDetails, PriceStructure, ShippingDetails, \
    ProductImage, PickUpWarehouseLocation



class ProductTypeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'
        

class CategoryViewSerializer(serializers.ModelSerializer):
    sub_category = ProductTypeViewSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'



class PriceStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceStructure
        fields = '__all__'


class PickUpWarehouseLocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PickUpWarehouseLocation
        fields = '__all__'

class ShippingDetailsSerializer(serializers.ModelSerializer):
    
    warehouse_pickup_location = PickUpWarehouseLocationSerializer(many=True, read_only=True)

    class Meta:
        model = ShippingDetails
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ServiceRegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRegions
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    product_variant_price_structure = PriceStructureSerializer(read_only=True)
    product_variant_shipping_details = ShippingDetailsSerializer(read_only=True)
    product_variant_image = ProductImageSerializer(many=True ,read_only=True)

    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductBelongDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBelongDetails
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(many=True, read_only=True)
    product_service_regions = ServiceRegionsSerializer(read_only=True)
    product_belong_details = ProductBelongDetailsSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        nested_representation = {
            'product_data': representation,
            'product_variant_data': representation.pop('product_variant', []),
            'service_regions_data': representation.pop('product_service_regions', {}),
            'product_belong_data': representation.pop('product_belong_details', {}),
            'pickup_locations' : representation.pop('warehouse_pickup_location', [])
        }
        return nested_representation
