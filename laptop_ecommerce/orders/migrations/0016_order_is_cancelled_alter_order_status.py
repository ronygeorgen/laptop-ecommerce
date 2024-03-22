# Generated by Django 5.0.2 on 2024-03-22 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Awaiting payment', 'Awaiting payment'), ('Confirmed', 'Confirmed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='New', max_length=20),
        ),
    ]
