# Generated by Django 5.0.2 on 2024-02-13 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_rename_my_category_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
