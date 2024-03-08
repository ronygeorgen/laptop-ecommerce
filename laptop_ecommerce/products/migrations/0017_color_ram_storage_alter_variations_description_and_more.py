# Generated by Django 5.0.2 on 2024-03-06 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_variations_color_alter_variations_product_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ram', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='variations',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='variations',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='variations',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.color'),
        ),
        migrations.AlterField(
            model_name='variations',
            name='ram',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.ram'),
        ),
        migrations.AlterField(
            model_name='variations',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.storage'),
        ),
    ]