from django.db import models
from main.models import Location


class FoodVendor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='vendor_logos/', null=True, blank=True)
    locations = models.ManyToManyField(Location, related_name='vendors')
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name
