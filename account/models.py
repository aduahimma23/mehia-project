from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    ADMIN = 1
    DELIVERY_MANAGER = 2
    CUSTOMER = 3
    DELIVERY_STAFF = 4
    INTERN_STAFF = 5

    USER_TYPE_CHOICES = [
        (ADMIN, "Admin"),
        (DELIVERY_MANAGER, "Delivery Manager"),
        (CUSTOMER, "Customer"),
        (DELIVERY_STAFF, "Delivery Staff"),
        (INTERN_STAFF, "Intern Staff"),
    ]

    user_type = models.IntegerField(default=CUSTOMER, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()
    
class DeliveryManagerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='delivery_manager_profile')
    phone_number = models.CharField(max_length=15)

class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

class DeliveryStaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='delivery_staff_profile')
    vehicle_number = models.CharField(max_length=20)

class InternStaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='intern_staff_profile')
    department = models.CharField(max_length=50)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == CustomUser.DELIVERY_MANAGER:
            DeliveryManagerProfile.objects.create(user=instance)
        elif instance.user_type == CustomUser.CUSTOMER:
            CustomerProfile.objects.create(user=instance)
        elif instance.user_type == CustomUser.DELIVERY_STAFF:
            DeliveryStaffProfile.objects.create(user=instance)
        elif instance.user_type == CustomUser.INTERN_STAFF:
            InternStaffProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == CustomUser.DELIVERY_MANAGER and hasattr(instance, 'delivery_manager_profile'):
        instance.delivery_manager_profile.save()
    elif instance.user_type == CustomUser.CUSTOMER and hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
    elif instance.user_type == CustomUser.DELIVERY_STAFF and hasattr(instance, 'delivery_staff_profile'):
        instance.delivery_staff_profile.save()
    elif instance.user_type == CustomUser.INTERN_STAFF and hasattr(instance, 'intern_staff_profile'):
        instance.intern_staff_profile.save()