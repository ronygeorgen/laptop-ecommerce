# Generated by Django 5.0.2 on 2024-03-06 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_variations_modified_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variations',
            name='modified_date',
        ),
    ]