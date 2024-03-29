# Generated by Django 5.0.2 on 2024-03-19 07:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer_management', '0003_remove_productoffer_product_offer_image'),
        ('products', '0023_alter_variations_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoffer',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.myproducts'),
        ),
    ]
