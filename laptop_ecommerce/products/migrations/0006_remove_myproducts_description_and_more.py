# Generated by Django 5.0.2 on 2024-03-02 02:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_variations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myproducts',
            name='description',
        ),
        migrations.RemoveField(
            model_name='myproducts',
            name='images',
        ),
        migrations.RemoveField(
            model_name='myproducts',
            name='price',
        ),
        migrations.RemoveField(
            model_name='myproducts',
            name='stock',
        ),
        migrations.AddField(
            model_name='variations',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='variations',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='variations',
            name='stock',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/variations')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variations')),
            ],
        ),
        migrations.AddField(
            model_name='variations',
            name='images',
            field=models.ManyToManyField(blank=True, to='products.image'),
        ),
    ]
