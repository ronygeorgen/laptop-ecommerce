# Generated by Django 5.0.2 on 2024-02-25 18:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_myproducts_is_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_category', models.CharField(choices=[('color', 'color'), ('ram', 'ram'), ('storage', 'storage')], max_length=100)),
                ('variation_values', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.myproducts')),
            ],
        ),
    ]