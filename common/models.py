from django.db import models

# Create your models here.

from django.db import models

class ModelMixin(models.Model):
    # user
    created_by = models.UUIDField(null=True, blank=True, help_text="User Id who created this record.")
    updated_by = models.UUIDField(null=True, blank=True, help_text="User Id who updated this record.")
    # datetime
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, help_text="Date and time at which this record is created")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, help_text="Date and time at which this record is last updated.")

    class Meta:
        abstract = True
