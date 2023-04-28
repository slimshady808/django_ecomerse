# Generated by Django 4.1.7 on 2023-04-16 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('COD', 'COD'), ('ONLINE_PAYMENT', 'ONLINE_PAYMENT')], default='COD', max_length=200, null=True),
        ),
    ]
