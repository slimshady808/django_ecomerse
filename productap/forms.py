from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductVariation

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'brand', 'slug', 'description', 'price', 'image', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ['image', 'image2', 'stock', 'type', 'variation_value']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
        }

ProductVariationFormSet = inlineformset_factory(Product, ProductVariation, form=ProductVariationForm, extra=1, can_delete=True)
