# Generated by Django 5.0.2 on 2024-03-19 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productoffer',
            old_name='discount_percentage',
            new_name='discount_rate',
        ),
    ]
