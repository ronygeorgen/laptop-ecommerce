# Generated by Django 5.0.2 on 2024-03-19 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer_management', '0002_rename_discount_percentage_productoffer_discount_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productoffer',
            name='product_offer_image',
        ),
    ]