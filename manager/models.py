from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from main.models import *

# Create your models here.
manager_group, created = Group.objects.get_or_create(name='manager')

# Get the content type for the Product model
content_type = ContentType.objects.get_for_model(Product)

# Assign permissions to the manager group
add_product_permission = Permission.objects.get(codename='add_product')
change_product_permission = Permission.objects.get(codename='change_product')

manager_group.permissions.add(add_product_permission, change_product_permission)