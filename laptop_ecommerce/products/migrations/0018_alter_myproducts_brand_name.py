# Generated by Django 5.0.2 on 2024-03-06 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_color_ram_storage_alter_variations_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myproducts',
            name='brand_name',
            field=models.CharField(max_length=100),
        ),
    ]