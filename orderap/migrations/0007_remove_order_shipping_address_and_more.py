# Generated by Django 4.1.7 on 2023-04-27 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderap', '0006_alter_order_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
