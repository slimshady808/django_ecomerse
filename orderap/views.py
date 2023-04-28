import json
from userap.models import Address
from cartap.models import cart,Coupon
from productap.models import Product,ProductVariation
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Order, OrderItem
from django.db.models import F

# Create your views here.



def order_detail(request,order_id):
    user=request.user
    order=Order.objects.get(id=order_id)
    
    address=json.loads(order.shipping_address)
    # return render(request,'confirmation.html',{'order':order})
    return render(request,'confirmation.html',{'order':order,'address':address})




@login_required
def create_order(request):
    if request.method == 'POST':
        user = request.user
        # is_paid = bool(request.POST.get('is_paid'))
        payment_status = request.POST.get('payment_status')
        if payment_status == 'COD':
            is_paid =False
        else:
            is_paid=True
        
        address_id = request.POST.get('address_id')
        # Check if an address was selected
        if not address_id:
            messages.error(request, 'Please select an address.')
            return redirect('check_out')
        shipping_address = Address.objects.get(id=address_id)
        shipping_address_dict={
            'name':shipping_address.name,
            'mobile':shipping_address.mobile,
            'house_name':shipping_address.house_name,
            'street':shipping_address.street,
            'district':shipping_address.district,
            'state':shipping_address.state,
            "pincode":shipping_address.pincode

        }
        shipping_address_json = json.dumps(shipping_address_dict)
        print(shipping_address_json)
        print(type(shipping_address_json))
        
        var_id=request.POST.get('var_id')
        variaton=ProductVariation.objects.get(id=var_id)
        total_amount = request.POST.get('total_amount')
        shipping_cost = request.POST.get('shipping_amount')
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            
        except Coupon.DoesNotExist:
            coupon = None
        
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address_json,
            date_ordered=timezone.now(),
            status='Pending',
            coupon=coupon,
            total_amount=total_amount,
            shipping_cost=shipping_cost,
            is_paid=is_paid,
            payment_status=payment_status,
            order_number=''
        )

        last_order = Order.objects.last()
        if last_order:
            last_order_number = last_order.order_number.split('-')[1]
            order_number = 'ORD-' + str(int(last_order_number) + 1)
        else:
            order_number = 'ORD-1'
        order.order_number = order_number
        order.save()
        cart_items =cart.objects.filter(user=user)
        for cart_item in cart_items:
            OrderItem.objects.create(
                product=cart_item.product,
                order=order,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                variation=variaton
            )
            # Update the stock of the selected variation
            variaton.stock = F('stock') - cart_item.quantity
            variaton.save()
        cart.objects.filter(user=user).delete()  # Clear the cart
        return redirect(reverse('order_detail', args=[order.id]))  # Redirect to order success page
    else:
        return redirect('checkout')  # Redirect to checkout page if not a POST request

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.cancel_order()
    return redirect('order_history')