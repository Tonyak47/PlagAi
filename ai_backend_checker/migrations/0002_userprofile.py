# Generated by Django 4.2.19 on 2025-03-02 23:48

import ai_backend_checker.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ai_backend_checker", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True,
                        default="default.png",
                        null=True,
                        upload_to=ai_backend_checker.models.user_directory_path,
                    ),
                ),
                (
                    "cropping",
                    image_cropping.fields.ImageRatioField(
                        "profile_picture",
                        "300x300",
                        adapt_rotation=False,
                        allow_fullsize=False,
                        free_crop=False,
                        help_text=None,
                        hide_image_field=False,
                        size_warning=False,
                        verbose_name="cropping",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
