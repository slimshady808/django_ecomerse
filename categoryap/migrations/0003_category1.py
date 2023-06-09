# Generated by Django 4.1.7 on 2023-04-06 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categoryap', '0002_category_cat_image_category_is_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('cat_image', models.ImageField(blank=True, upload_to='photos/categories')),
                ('is_available', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
    ]
