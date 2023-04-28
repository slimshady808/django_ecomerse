from django.shortcuts import render,redirect
from .models import Product,cart,ProductVariation
from django.db.models import Q
from django.http import JsonResponse
from django.http import  HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# add to cart 
@login_required(login_url='log_in')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    variant_id = request.GET.get('var_id')

    if variant_id:
        variant_id = variant_id.strip('[]').strip("'")
        variant = ProductVariation.objects.get(id=int(variant_id))

    # Check if this product/variation is already in the user's cart
    cart_items = cart.objects.filter(user=user, product=product)
    if variant_id:
        cart_items = cart_items.filter(variations=variant)

    if cart_items.exists():
        # If the user already has this product/variation in their cart, don't add it again
        messages.warning(request, "This product is already in your cart.")
    else:
        # Otherwise, add the product/variation to the user's cart
        new_cart_item = cart.objects.create(user=user, product=product)
        if variant_id:
            new_cart_item.variations.add(variant)
        new_cart_item.save()
        messages.success(request, "Product added to cart.")

    return redirect('show_cart')


#show cart
@login_required(login_url='log_in')
def show_cart(request):
    user = request.user
    cart_products = cart.objects.filter(user=user)

    amount = 0
    shipping_amount = 70
    total_amount = 0
    variations = None

    # Check if there are any products in the cart
    if cart_products.exists():
        for cart_product in cart_products:
            if cart_product.quantity == 0:  # Check if cart quantity is 0
                cart_product.quantity = 1  # Set cart quantity to 1
                cart_product.save()
            if cart_product.variations.exists():
                variations = list(cart_product.variations.all())
                for variation in variations:
                    if variation.stock < cart_product.quantity:
                        # If cart quantity is more than stock, set cart quantity to available stock
                        cart_product.quantity = variation.stock
                        cart_product.save()
            else:
                variations = None

            # Calculate cart amount and total amount
            temp_amount = (cart_product.quantity * cart_product.product.price)
            amount += temp_amount
            total_amount = amount + shipping_amount

        return render(request, 'cart/cart.html', {
            'carts': cart_products,
            'total_amount': total_amount,
            'amount': amount,
            'variations': variations,
        })
    else:
        return render(request, 'cart/emptycart.html')





# add the cart quantity
@login_required(login_url='log_in')
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        var_id = request.GET.get('var_id')
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user) & Q(variations__id=var_id))
        
        # Check if there is enough stock to add one more item to the cart
        variation = ProductVariation.objects.get(id=var_id)
       
           
       
        if variation.stock <= c.quantity:
            # If there is not enough stock, show a warning message to the user
            return JsonResponse({'error': f"Sorry, there are only {variation.stock} items left in stock."})
            
            # Return a JSON response with the current cart quantity and amount
            data = {
                'quantity': c.quantity,
                'amount': c.quantity * c.product.price,
                'total_amount': 0
            }
        else:
        
         c.quantity += 1 
         c.save()
        
        amount = 0
        shipping_amount = 70
        cart_product = cart.objects.filter(user=request.user)
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
            
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)



@login_required(login_url='log_in')
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        var_id = request.GET.get('var_id') # get the variation ID
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user) & Q(variations__id=var_id)) # get the cart object for the given product and variation
        c.quantity -= 1 
        
        if c.quantity > 0:
            c.save()
        else:
            c.delete()
            
        amount = 0
        shipping_amount = 70
        cart_product = cart.objects.filter(user=request.user)
        for p in cart_product:
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
          
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
        }
        return JsonResponse(data)
    
    
@login_required(login_url='log_in')
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        var_id = request.GET.get('var_id')
        
        try:
            c = cart.objects.filter(product=prod_id, user=request.user)
            if var_id:
                var_id = var_id.strip('[]').strip("'")
                c = c.filter(variations__id=var_id)
            c.delete()

            amount = 0
            shipping_amount = 70
            cart_product = [p for p in cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount += tempamount

            data = {
                'amount': amount,
                'total_amount': amount + shipping_amount
            }
            return JsonResponse(data)
        except cart.DoesNotExist:
            return HttpResponseBadRequest('Invalid product ID')
        except Exception as e:
            return HttpResponseBadRequest(str(e))

