from django import forms
from .models import Pricing, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class PricingForm(forms.ModelForm):
    class Meta:
        model = Pricing
        fields = '__all__'