import uuid
from django.db import models
from common import enums, validators
from app_user.models import User
from django.utils import timezone
from common.models import ModelMixin
from taggit.managers import TaggableManager
from app_dashboard.models import Cities, Country, States
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from app_inventory.queryset import ProductSectionQuerySet
from django.core.validators import MaxLengthValidator, MinValueValidator
# Create your models here.


class PickUpWarehouseLocation(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="inventory_warehouse_location")
    plot_no = models.CharField(max_length=255, null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    landmark = models.TextField(max_length=255, null=True, blank=True)
    state = models.ForeignKey(States, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(Cities, on_delete=models.DO_NOTHING)
    pin_code = models.CharField(max_length=6,validators=[validators.pin_validator], 
        null=True, blank=True)

    class Meta:
        verbose_name = _("Inventory - Pickup Warehouse Location")
        verbose_name_plural = _("Inventory - Pickup Warehouse Location")

    def __str__(self):
        return f"{self.seller.username} - {self.location_name}"
    
class Category(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='category', blank=True, null=True)

    class meta:
        verbose_name = _("Inventory - Category")
        verbose_name_plural = _("Inventory - Category")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
    
    
class ProductType(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,
        blank=True, related_name="product_types")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='product_type', blank=True, null=True)
    commission_type = models.CharField(max_length=25, choices=enums.CommissionTypeEnums.choices,
        default=enums.CommissionTypeEnums.COMMISSION_PERCENTAGE) 
    commission_value = models.IntegerField(blank=True, default=0)
    returnable_product = models.BooleanField(default=False, null=True)

    class meta:
        verbose_name = _("Inventory - Product Type")
        verbose_name_plural = _("Inventory - Product Type")
        unique_together = ("name", "category")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductType, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    

class Product(ModelMixin):
    # 0. basic details
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_title = models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE,related_name="seller_product")
    about_the_brand = models.CharField(max_length=225,blank=True,null=True)
    product_brand = models.CharField(max_length=255,blank=True, null=True)

    # 1. categoy and sub category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    product_has_variant = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False) 

    # 2. additional details (more info)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.CharField(max_length=3500, blank=True, null=True)
    warranty = models.CharField(max_length=100,
        choices=enums.WarrantyEnums.choices, blank=True,null=True)
    guarantee = models.CharField(max_length=100,
        choices=enums.GuaranteeEnums.choices, blank=True,null=True)
    material = models.CharField(max_length=225,blank=True,null=True)
    product_belong_to = models.CharField(max_length=125, choices=enums.ProductBelongEnums.choices, 
        default=enums.ProductBelongEnums.SEVENTHSQ)
    packaging_size = models.CharField(max_length=555,blank=True,null=True)
    components_per_unit = models.CharField(max_length=555,blank=True,null=True)

    # 2.2 ---- instructions
    product_handling = models.CharField(max_length=500,blank=True,null=True)
    installation = models.CharField(max_length=500,blank=True,null=True)
    storage = models.CharField(max_length=500,blank=True,null=True)
    usage = models.CharField(max_length=500,blank=True,null=True)

    # 4. shipping
    serviced_regions = models.CharField(max_length=255,
        choices=enums.ServicedRegionsEnums.choices, blank=True,null=True)
    shipping_include = models.BooleanField(default=False)

    minimum_order_qunatity = models.CharField(max_length=555,blank=True,null=True)
    minimum_order_qunatity_unit = models.CharField(max_length=555,
        choices=enums.MinimumOrderQuantityEnums.choices, blank=True,null=True)



    # gst_rate = models.CharField(max_length=100,blank=True,null=True)
    # packed_length = models.CharField(max_length=100,blank=True,null=True)
    # packed_width = models.CharField(max_length=100,blank=True,null=True)
    # packed_height = models.CharField(max_length=100,blank=True,null=True)
    # prod_commissions = models.CharField(max_length=100,blank=True,null=True)
    # Payment_gateway_charge = models.CharField(max_length=100,blank=True,null=True)
    # gst_on_product = models.CharField(max_length=100,blank=True,null=True)
    # our_commissions = models.CharField(max_length=100,blank=True,null=True)
    # final_price = models.CharField(max_length=100,blank=True,null=True)
    # default_sp = models.CharField(max_length=100,blank=True,null=True)
    # default_mp = models.CharField(max_length=100,blank=True,null=True)
    # default_var = models.CharField(max_length=100,blank=True,null=True)
    # net = models.CharField(max_length=100,blank=True,null=True)
    # select_variant_data = models.CharField(max_length=100,blank=True,null=True)
    # tag_variant = models.CharField(max_length=100,blank=True,null=True)
    # selected_variant_data = models.CharField(max_length=100,blank=True,null=True)
    # variant_mp_data = models.CharField(max_length=100,blank=True,null=True)
    # variant_sp_data = models.CharField(max_length=100,blank=True,null=True)
    # variant_on_request_all_data = models.CharField(max_length=100,blank=True,null=True)
    # var_is_default_all_data = models.CharField(max_length=100,blank=True,null=True)
    # product_dimension_unit_box = models.CharField(max_length=100,blank=True,null=True)
    # variant = models.CharField(max_length=500,blank=True,null=True)
    # product_tags = TaggableManager(verbose_name="product_tags",blank=True)
    # incl_gst = models.BooleanField(default=False,null=True)
    # views = models.FloatField(default=1)
    # mostsells = models.FloatField(default=1)
    # variant_name = models.CharField(max_length=128, null=True, blank=True)
    # variant_value = models.CharField(max_length=128, null=True, blank=True)
    # variant_default = models.BooleanField(default=False)
    # default_poq = models.CharField(max_length=100,blank=True,null=True)
    # marked = models.CharField(max_length=100,blank=True,null=True)
    # colors = models.CharField(max_length=100,default='',null=True,blank=True)
    # product_status = models.BooleanField(default=False)
    # shipping_with_seventh_square = models.BooleanField(default=True)
    # var_added = models.BooleanField(default=False)
    # qty = models.FloatField(validators=[MinValueValidator(0)])
    # qty_unit = models.CharField(max_length=555,blank=True,null=True)
    # marked_price = models.FloatField(default=0.0)
    # selling_price = models.FloatField(default=0.0)
    # commercial_price = models.FloatField(validators=[MinValueValidator(0)], default=0.0, blank=True,null=True)
    # discount = models.FloatField(blank=True,null=True)
    # objects = ProductSectionQuerySet.as_manager()

    class meta:
        verbose_name = _("Inventory - Add Product")
        verbose_name_plural = _("Inventory - Add Product")

    def __str__(self):
        return f"{self.id}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_title)
        super(Product, self).save(*args, **kwargs)
    

class ProductBelongDetails(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete = models.CASCADE, related_name="product_belong_details")
    product_fetch_id = models.CharField(max_length=225, null=True, blank=True)
    product_fetch_status = models.BooleanField(default=False)
    product_fetch_json = models.JSONField(default=dict, blank=True, null=True)

    class meta:
        verbose_name = _("Inventory - Product Belong Details")
        verbose_name_plural = _("Inventory - Product Belong Details")

    def __str__(self):
        return f"{self.product__id} - {self.product_fetch_id}"
      

class ProductVariant(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_variant")
    name = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255,  null=True, blank=True)
    price_on_request = models.BooleanField(default=False)
    default_variant = models.BooleanField(default=False)

    class meta:
        verbose_name = _("Inventory - Add Product Variant")
        verbose_name_plural = _("Inventory - Add Product Variant")

    def __str__(self):
        return f"{self.product} - {self.id}"


class ProductImage(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE,
        related_name="product_variant_image")
    picture = models.FileField(upload_to='picture', blank=True,null=True)

    class meta:
        verbose_name = _("Inventory - Add Photo")
        verbose_name_plural = _("Inventory - Add Photo")

    def __str__(self):
        return f"{self.picture}"
    

class ServiceRegions(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE,
        related_name="product_service_regions") 
    serviced_regions_description = models.CharField(default=True,blank=True, null=True)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)

    class meta:
        verbose_name = _("Inventory - Add Service Regions")
        verbose_name_plural = _("Inventory - Add Service Regions")

    def __str__(self):
        return f"{self.serviced_regions_description}"
    

class PriceStructure(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE,
        related_name="product_variant_price_structure")
    hsn_code = models.CharField(max_length=8,blank=True,null=True)
    sale_price = models.CharField(max_length=100,blank=True,null=True)
    mrp = models.CharField(max_length=100, blank=True, null=True)
    tax_code = models.CharField(max_length=100, 
        choices=enums.TaxCodeEnums.choices, blank=True, null=True) 
    class meta:
        verbose_name = _("Inventory - Add Price Structure")
        verbose_name_plural = _("Inventory - Add Price Structure")
    
    def __str__(self):
        return f"{self.sale_price}"


class ShippingDetails(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE,
        related_name="product_variant_shipping_details")
    pick_up_location = models.ManyToManyField(PickUpWarehouseLocation,
        related_name='warehouse_pickup_location')
    product_weight = models.CharField(max_length=125, blank=True,null=True)
    product_weight_unit = models.CharField(max_length=125,
        choices=enums.ProductWeighteEnums.choices,blank=True,null=True)
    returnable_product = models.BooleanField(default=False)
    return_policy = models.CharField(max_length =555,default=True,blank=True, null=True)
    shipping_method = models.CharField(max_length=100,
        choices=enums.ShippingMethodEnums.choices, blank=True,null=True)
    packed_box_dimensions_width = models.CharField(max_length=100,blank=True,null=True)
    packed_box_dimensions_unit = models.CharField(max_length=100,
        choices=enums.PackedBoxDimensionsUnitEnums.choices, blank=True,null=True)
    packed_box_dimensions_length = models.CharField(max_length=100,blank=True,null=True)
    packed_box_dimensions_height = models.CharField(max_length=100,blank=True,null=True)
    product_dimensions_length = models.CharField(max_length=50,blank=True,null=True)
    product_dimensions_width = models.CharField(max_length=50,blank=True,null=True)
    product_dimensions_height = models.CharField(max_length=50,blank=True,null=True)
    product_dimensions_unit = models.CharField(max_length=50,blank=True,null=True,
        choices=enums.ProductDimensionUnitEnums.choices)


    class meta:
        verbose_name = _("Inventory - Add Shipping Fields")
        verbose_name_plural = _("Inventory - Add Shipping Fields")
    
    def __str__(self):
        return f"{self.product_variant}"


