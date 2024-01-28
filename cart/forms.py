from django import forms
from .models import CartItems

class CartItemForm(forms.ModelForm):
    class meta:
        model = CartItems
        fields = ['quantity']