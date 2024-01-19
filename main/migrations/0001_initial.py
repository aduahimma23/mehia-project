# Generated by Django 5.0.1 on 2024-01-19 18:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliveryAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("street_address", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("description", models.CharField(blank=True, max_length=250)),
                ("price", models.FloatField()),
                ("pieces", models.IntegerField(default=6)),
                ("instructions", models.CharField(default="Available", max_length=250)),
                (
                    "image",
                    models.ImageField(default="default.png", upload_to="images/"),
                ),
                (
                    "labels",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("BestSeller", "BestSeller"),
                            ("New Food", "New Food"),
                        ],
                        max_length=25,
                    ),
                ),
                (
                    "label_colour",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("danger", "danger"),
                            ("success", "success"),
                            ("primary", "primary"),
                            ("info", "info"),
                            ("warning", "warning"),
                        ],
                        max_length=15,
                    ),
                ),
                ("slug", models.SlugField(default="foods")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
