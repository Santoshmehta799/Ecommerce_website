from django.db import models
from common import validators
from common.models import ModelMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.

class States(ModelMixin):
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

class Cities(ModelMixin):
    state = models.ForeignKey(States, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=225)
    pin_code = models.CharField(max_length=6,validators=[validators.pin_validator], 
        null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.state.name} - {self.pin_code}"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Dashboard - City Details')
        verbose_name_plural = _('Dashboard - City Details')
        unique_together = ('state','name')




