from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from orderap.models import Order

User = get_user_model()

class Sales(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sales_reports',null=True)
    order_number = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Sales Reports"
        ordering = ['-order_date']

    def __str__(self):
        return self.order_number
