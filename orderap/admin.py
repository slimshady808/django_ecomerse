from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number','id', 'user', 'date_ordered', 'status', 'payment_status', 'total_amount', 'is_paid')
    list_filter = ('status', 'is_paid')
    inlines = [OrderItemInline]
    list_editable = ('status', )

    def status(self, obj):
        return obj.status

    def payment_status(self, obj):
        return obj.payment_status

    status.admin_order_field = 'status'
    payment_status.admin_order_field = 'payment_status'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'price', 'variation')
    list_filter = ('product', 'order', 'variation')


