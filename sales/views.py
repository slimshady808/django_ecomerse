from django.shortcuts import render
from django.utils import timezone
from .models import Order, Sales

def sales(request):
    # Retrieve all orders with status "Delivered"
    delivered_orders = Order.objects.filter(status='Delivered')

    # Create SalesReport objects for each order
    for order in delivered_orders:
        # Try to fetch an existing sales report for this order
        sales_report, created = Sales.objects.get_or_create(
            order=order,  # Set the order field to the corresponding Order object
            order_number=order.order_number,
            user=order.user,
            defaults={
                'total_amount': order.total_amount,
                'order_date': order.date_ordered
            }
        )

        # Update the sales report if it already exists
        if not created:
            sales_report.total_amount = order.total_amount
            sales_report.order_date = order.date_ordered
            sales_report.save()

    # Render a success message
    context = {'message': 'Sales report generated successfully'}
    return render(request, 'new.html', context)

