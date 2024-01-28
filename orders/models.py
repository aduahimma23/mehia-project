from django.db import models
from main.models import *
from menu.models import Product

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('pending', 'Pending'), ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'), ('delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'order {self.id} - {self.user.username}'
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)


    def sub_total(self):
        return self.quantity * self.item_price
    

class OrderAssignment(models.Model):
    deliverer = models.ForeignKey(Deliverer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    acceptance_time = models.DateTimeField(null=True, blank=True)
    delivered_time = models.DateTimeField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def accept_order(self):
        if not self.is_accepted and self.deliverer.is_avalable:
            self.is_accepted = True
            self.acceptance_time = timezone.now()
            self.deliverer.is_avalable = True
            self.deliverer.last_acceptance = timezone.now()
            self.deliverer.save()
            self.save()

    def reject_order(self):
        if not self.is_accepted:
            self.is_accepted = False
            self.acceptance_time = timezone.now()
            self.save()

    def mark_delivered(self):
        if self.is_accepted and not self.is_delivered:
            self.is_delivered = True
            self.delivered_time = timezone.now()
            self.deliverer.is_available = True
            self.deliverer.save()
            self.save()


class OrderTracking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('in_progress', 'In Progress'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_staff = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_staff')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)
    location_lat = models.FloatField(null=True, blank=True)
    location_lon = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order tracking - {self.order}'
    
    class Meta:
        ordering = ['-created_at']
