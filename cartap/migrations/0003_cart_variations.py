# Generated by Django 4.1.7 on 2023-04-09 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productap', '0002_alter_productvariation_unique_together'),
        ('cartap', '0002_coupon_cart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='variations',
            field=models.ManyToManyField(to='productap.productvariation'),
        ),
    ]
