from django import forms
from app_inventory.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__' 
