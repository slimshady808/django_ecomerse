# Generated by Django 4.1.7 on 2023-04-01 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='mobile_number',
            field=models.CharField(default='', max_length=20),
        ),
    ]
