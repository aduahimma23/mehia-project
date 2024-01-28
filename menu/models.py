from django.db import models
from main.models import *

    
class Category(models.Model):
    name_of_category = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"{self.name_of_category}"
    

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, unique=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    LABELS = (
        ('Best Seller', 'BestSeller'),
        ('New Food', 'New Food'),
    )   

    LABEL_COLOUR = (
        ('danger', 'danger'),
        ('success', 'success'),
    )
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=250,blank=True)
    size = models.BooleanField(default=True)
    small = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    regular = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    medium = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    large = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_large = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_file = models.ImageField(default='default.png', upload_to='images/product')
    labels = models.CharField(max_length=25, choices=LABELS, blank=True)
    label_colour = models.CharField(max_length=15, choices=LABEL_COLOUR, blank=True)
    slug = models.SlugField(default="foods")

    def set_size(self, requires_size_selection):
            if self.size and requires_size_selection:
                self.small = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
                self.regular = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
                self.medium = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
                self.large = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
                self.extra_large = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
            else:
                self.small = None
                self.regular = None
                self.medium = None
                self.large = None
                self.extra_large = None


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Pricing(models.Model):
    food_item = models.OneToOneField(Product, on_delete=models.CASCADE)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def set_discount(self, discount_percent):
        if self.discounted_price is None:
            discount_amount = (self.regular_price * discount_percent) / 100
            self.discounted_price = self.regular_price - discount_amount
            self.save()
            return self.discounted_price
        else:
            return self.discounted_price

    def __str__(self):
        return f"Pricing for {self.food_item.name}"
    
    def apply_promotion(self, promotion):
        if promotion.start_date <= self.start_date <= promotion.end_date or promotion.start_date <= self.end_date <= promotion.end_date:
            # Apply the discount
            self.discounted_price = self.regular_price - ((self.regular_price * promotion.discount_percent) / 100)
            self.save()
            return True
        return False


class ExtraItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    add_extra_items = models.BooleanField(default=False)
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def add_extra(self):
        if not self.add_extra_items:
            self.name = ''
            self.price = 0.0
        super().save(*self.name, * self.price)


class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name  