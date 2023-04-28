from django.db import models

# Create your models here.

from django.utils import timezone

class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banners/')
    link = models.CharField(max_length=200, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title