from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'user_type']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
