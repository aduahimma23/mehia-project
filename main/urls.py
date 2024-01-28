from django.urls import path
from .views import *


app_name = 'main'

urlpatterns = [
    path('home/', home, name='home'),
    path('contact/', contact, name='contact'),
    path('menu/', menu, name='menu'),
    path('about/', about, name='about'),
]