import uuid
from common import enums
from django.db import models
from common.models import ModelMixin
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Blog(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    body = RichTextField(blank=True,null=True)
    image = models.ImageField(upload_to = 'blogs')
    author = models.CharField(max_length=60,default="theseventhsquare")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    Blog_type = models.CharField(max_length=16, choices=enums.ChoicesBlogTypeEnums.choices, null=True)
    
    class meta:
        verbose_name = _("Context - Blog")
        verbose_name_plural = _("Context - Blog")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class FaqMain(ModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=500, null=True, blank=True)
    answer = RichTextField(blank=True, null=True)
    author = models.CharField(max_length=60, default="theseventhsquare")
    tage_type = models.CharField(max_length=100, choices=enums.ChoicesTypeEnums.choices, null=True)

    class meta:
        verbose_name = _("Context - Faq Main")
        verbose_name_plural = _("Context - Faq Main")

    def __str__(self):
        return self.question



