from django.db import models
from django.contrib.auth.models import User
from productap.models import Product,ProductVariation
# Create your models here.

class Whishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
      return f"{self.product} ({self.user})"