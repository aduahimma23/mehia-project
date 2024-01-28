from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django.utils import timezone
from account.models import CustomUser
from menu.models import Product

class Location(models.Model):
    """"Taking the location of the food vendor"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# user delivery address
class DeliveryAddress(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Delivery Address"


class Reviews(models.Model):
    CustomUser = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    item = models.ForeignKey(Product, on_delete = models.CASCADE)
    rslug = models.SlugField()
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.review
    

class Deliverer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    is_avalable = models.BooleanField(default=True)
    last_acceptance = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name