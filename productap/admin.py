from django.contrib import admin
from .models import Product, ProductVariation

class ProductVariationsInline(admin.TabularInline):
    model = ProductVariation
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')
    list_filter = ('category', 'available')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariationsInline]

class ProductVariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_value', 'type', 'stock')
    list_filter = ('product', 'type')
    list_editable = ('variation_value', 'stock')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariation, ProductVariationsAdmin)
