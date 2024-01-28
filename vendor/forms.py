from django import forms
from .models import FoodVendor
from main.models import Location
from menu.models import FoodItem

class FoodVendorForm(forms.ModelForm):
    class Meta:
        model = FoodVendor
        fields = ['name', 'description', 'logo', 'locations', 'phone_number', 'email', 'menu']

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Enter your phone number'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'custom-class', 'rows': 4, 'placeholder': 'Enter vendor description'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Enter phone number'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'custom-class', 'placeholder': 'Enter email address'}), label='Email')
    website = forms.URLField(widget=forms.URLInput(attrs={'class': 'custom-class', 'placeholder': 'Enter website URL'}), label='Website')
    locations = forms.ModelMultipleChoiceField(queryset=Location.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-class'}), label='Locations')
    menu = forms.ModelMultipleChoiceField(queryset=FoodItem.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-class'}), label='Menu Items')