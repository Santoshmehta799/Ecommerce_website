from django.db import models
from common import validators
from common.models import ModelMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Country(ModelMixin):
    name = models.CharField(max_length=255,unique=True)
    iso2_code = models.CharField(max_length=10, null=True, blank=True)
    iso3_code = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.upper()
            self.iso2_code = self.iso2_code.upper()
            self.iso3_code = self.iso3_code.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Dashboard - Country Details')
        verbose_name_plural = _('Dashboard - Country Details')
    
    
class States(ModelMixin):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=225,unique=True)
    state_code = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Dashboard - State Details')
        verbose_name_plural = _('Dashboard - State Details')
        unique_together = ('country','name')

class Cities(ModelMixin):
    state = models.ForeignKey(States, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=225)
    pin_code = models.CharField(max_length=6,validators=[validators.pin_validator], 
        null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Dashboard - City Details')
        verbose_name_plural = _('Dashboard - City Details')
        unique_together = ('state','name')




