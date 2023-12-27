import uuid
from django.db import models
from app_dashboard.models import Cities, States
from app_user.models import User
from common import validators
from common.models import ModelMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.


class PickUpWarehouseLocation(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="inventory_warehouse_location")
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
        return f"{self.user.username} - {self.location_name}"
    
class Category(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    image = models.ImageField(upload_to='category', blank=True,null=True,default='')
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)

    class meta:
        verbose_name = _("Inventory - Category")
        verbose_name_plural = _("Inventory - Category")
    
    def __str__(self):
        return f"{self.name}"
    
class ProductType(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='product_type', blank=True,null=True,default='')
    commission_type = models.CharField(max_length=25)
    commission_value = models.IntegerField(blank=True, default=0)
    returnable_product = models.BooleanField(default=False, null=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True, null=True)

    class meta:
        verbose_name = _("Inventory - Product Type")
        verbose_name_plural = _("Inventory - Product Type")
        unique_together = ("name", "category")

    def __str__(self):
        return f"{self.name}"
    
# class Product(ModelMixin):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    

    
