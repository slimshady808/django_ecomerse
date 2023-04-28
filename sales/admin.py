# from django.contrib import admin
# from .models import Sales
# from import_export.admin import ExportMixin
# #from import_export_pdf.admin import ExportPdfMixin
# class SalesAdmin(ExportMixin,admin.ModelAdmin):
#     list_display = ('order_number', 'customer_name', 'total_amount', 'order_date')
#     search_fields = ['order_number', 'customer_name']
#     list_filter = ('order_date',)
#     date_hierarchy = 'order_date'

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.filter(order__status='Delivered')

#     def order_number(self, obj):
#         return obj.order_number
#     order_number.short_description = "Order Number"

#     def customer_name(self, obj):
#         return obj.order.user.username
#     customer_name.short_description = "Customer Name"

#     def total_amount(self, obj):
#         return obj.total_amount
#     total_amount.short_description = "Total Amount"

#     def order_date(self, obj):
#         return obj.order_date
#     order_date.admin_order_field = 'order_date'
#     order_date.short_description = "Order Date"

# admin.site.register(Sales, SalesAdmin)



