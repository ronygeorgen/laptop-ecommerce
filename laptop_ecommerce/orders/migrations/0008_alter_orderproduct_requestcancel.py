# Generated by Django 5.0.2 on 2024-03-11 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_orderproduct_requestcancel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='requestcancel',
            field=models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], default='No', max_length=30),
        ),
    ]
