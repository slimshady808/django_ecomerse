from django.db import models
from productap.models import Product,ProductVariation
from userap.models import Address
from cartap.models import Coupon
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import json
# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('COD', 'COD'),
        ('ONLINE_PAYMENT','ONLINE_PAYMENT'),
        ('PayPal','PayPal')
       
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.JSONField(null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS_CHOICES, default='Pending')
    payment_status=models.CharField(max_length=200, null=True, choices=PAYMENT_CHOICES, default='COD')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    order_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.last()
            if last_order:
                last_order_number = last_order.order_number.split('-')[1]
                self.order_number = 'ORD-' + str(int(last_order_number) + 1)
            else:
                self.order_number = 'ORD-1'
        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.id)
    
    def cancel_order(self):
        self.status = 'Cancelled'
        self.save()

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total