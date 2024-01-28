from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/<int:product>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', view_cart, name='cart_view'),
    path('udate-cart/int:cart_item_id>/', update_cart, name='update_cart'),
]