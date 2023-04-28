
from django.db import models
from categoryap.models import Category
from django.core.validators import MinValueValidator
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default='')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='photos/products', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='photos/variations', blank=True)
    image2 = models.ImageField(upload_to='photos/variations', blank=True)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    TYPE_CHOICES = (
        ('size', 'Size'),
        ('storage', 'Storage'),
        ('color', 'Color'),
        ('style', 'Style'),
        ('model', 'Model'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES,default='')
    variation_value = models.CharField(max_length=255,default='')
    class Meta:
        unique_together = ('product', 'variation_value')

    def __str__(self):
        return f"{self.product.name} - {self.variation_value} - {self.get_type_display()}"



















