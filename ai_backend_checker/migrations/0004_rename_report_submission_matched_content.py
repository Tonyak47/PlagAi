# Generated by Django 5.1.4 on 2025-03-23 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ai_backend_checker', '0003_reference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='report',
            new_name='matched_content',
        ),
    ]
