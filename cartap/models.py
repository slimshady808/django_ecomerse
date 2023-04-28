from django.db import models
from django.contrib.auth.models import User
from productap.models import Product,ProductVariation
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    minimum_amount=models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.code



class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    variations = models.ManyToManyField(ProductVariation)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self) :
        return str(self.id)