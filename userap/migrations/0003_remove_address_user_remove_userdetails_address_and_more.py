# Generated by Django 4.1.7 on 2023-04-01 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userap', '0002_userdetails_mobile_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='user_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userap.userdetails'),
        ),
    ]