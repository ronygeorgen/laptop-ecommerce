# Generated by Django 5.0.2 on 2024-03-12 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_alter_wallet_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
