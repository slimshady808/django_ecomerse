from django.contrib import admin
from .models import cart, Coupon

class cartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_filter = ['user']
    search_fields = ['user__username', 'product__name']

admin.site.register(cart, cartAdmin)




@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'active')
    list_filter = ('active',)
    search_fields = ('code',)

