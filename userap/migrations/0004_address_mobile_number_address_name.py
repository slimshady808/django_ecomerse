# Generated by Django 4.1.7 on 2023-04-13 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userap', '0003_remove_address_user_remove_userdetails_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='mobile_number',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
