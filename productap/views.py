from django.shortcuts import get_object_or_404, render,redirect
from .models import Product,Category,ProductVariation
from userap.models import Address,UserDetails
from cartap.models import cart,Coupon
from django.contrib import messages
from banner.models import Banner
# Create your views here.

def home(request):
    categories = Category.objects.all()
    products = Product.objects.order_by('-id')[:8]

    banners = Banner.objects.all()
    return render(request, 'products/index.html', {'categories': categories, 'products': products,'banners':banners})

def product_view(request):
  return render(request,'products/single_product.html')
#===========================================
from django.core.paginator import Paginator

def view_item(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variations = product.variations.all()
    selected_var = request.GET.getlist('var')
    
    va_name=None
    va_stock=None
    if len(selected_var) > 0:
        variation_image = None
        
        variation = []
        for var_id in selected_var:
            vari=var_id
            
            var = get_object_or_404(ProductVariation, id=var_id, product=product)
            variation.append(var)
            print(variation)
            if var.image:
                variation_image = var.image
                va_name=var.variation_value
                va_stock=var.stock
    else:
        variation = None
        variation_image = product.image

    all_products = Product.objects.filter(category=product.category)
    paginator = Paginator(all_products, 3)  # Show 3 products per page

    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {
        'product': product,
        'variations': variations,
        'selected_variations': variation,
        'variation_image': variation_image,
        'products': products,
        'selected_var':selected_var,
        'va_name':va_name,
        'va_stock':va_stock
    }
    return render(request, 'products/viewproduct.html', context)




#====================================================



   
#=======================================================

def check_out_add_address(request):
    user = request.user
    user_details = UserDetails.objects.get(user=user)
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        house_name = request.POST.get('house_name')
        street = request.POST.get('street')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        if not (name and mobile and house_name and street and district and state and pincode):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('check_out')
        address = Address.objects.create(
            user_details=user_details,
            name=name,
            mobile=mobile,
            house_name=house_name,
            street=street,
            district=district,
            state=state,
            pincode=pincode,
         )
        messages.success(request, 'Address added successfully.')
        return redirect('check_out')








def check_out(request):
   user = request.user
   user_details = UserDetails.objects.get(user=user)
   addresses = Address.objects.filter(user_details=user_details)
   cart_items = cart.objects.filter(user=user)
   amount = 0
   shipping_amount = 70
   total_amount = 0
   cart_products = [p for p in cart.objects.all() if p.user == request.user]
   temp_amount_list=[]
   if cart_products:
       for p in cart_products:
            
            if p.quantity <= 0 or p.variations.get().stock <=0:
                messages.error(request, 'Remove the item "' + str(p.product) + '" from your cart. It is out of stock.')
                return redirect('show_cart')
            temp_amount = p.quantity * p.product.price
            amount += temp_amount
            temp_amount_list.append(temp_amount)
            if p.variations.exists():
                
                variations=list(p.variations.all())
                
            else:
                variations=None
            
       if amount >1500:
           shipping_amount=0
       total_amount = amount + shipping_amount
   else:
       return redirect('show_cart')  
           
   # handle coupon redemption
   coupon_code = request.POST.get('coupon_code')
   coupon_discount = 0
   if coupon_code:
       try:
           coupon = Coupon.objects.get(code=coupon_code)
           coupon_discount = coupon.discount
           total_amount -= coupon_discount
       except Coupon.DoesNotExist:
           messages.error(request, 'Invalid coupon code.')
   # zip the cart_items and temp_amount_list into a list of tuples
   cart_items_with_temp_amount = zip(cart_items, temp_amount_list)
   return render(request, 'checkout.html', {
       'addresses': addresses,
       'cart_items': cart_items,
       'amount': amount,
       'shipping_amount': shipping_amount,
       'total_amount': total_amount,
       'temp_amount_list':temp_amount_list,
       'coupon_discount': coupon_discount,
       'cart_items_with_temp_amount': cart_items_with_temp_amount, # pass the zipped list to the template
       'variations': variations ,
       'coupon_code':coupon_code
   })


def check_out1(request):
   user = request.user
   user_details = UserDetails.objects.get(user=user)
   addresses = Address.objects.filter(user_details=user_details)
   cart_items = cart.objects.filter(user=user)
   amount = 0
   shipping_amount = 70
   total_amount = 0
   cart_products = [p for p in cart.objects.all() if p.user == request.user]
   temp_amount_list=[]
   if cart_products:
       for p in cart_products:
            temp_amount = p.quantity * p.product.price
            amount += temp_amount
            temp_amount_list.append(temp_amount)
            if p.variations.exists():
                variations=list(p.variations.all())
            else:
                variations=None
            print(variations)
       if amount >1500:
           shipping_amount=0
       total_amount = amount + shipping_amount
       
           
   # handle coupon redemption
   coupon_code = request.POST.get('coupon_code')
   coupon_discount = 0
   if coupon_code:
       try:
           coupon = Coupon.objects.get(code=coupon_code)
           coupon_discount = coupon.discount
           total_amount -= coupon_discount
       except Coupon.DoesNotExist:
           messages.error(request, 'Invalid coupon code.')
   # zip the cart_items and temp_amount_list into a list of tuples
   cart_items_with_temp_amount = zip(cart_items, temp_amount_list)
   return render(request, 'checkout1.html', {
       'addresses': addresses,
       'cart_items': cart_items,
       'amount': amount,
       'shipping_amount': shipping_amount,
       'total_amount': total_amount,
       'temp_amount_list':temp_amount_list,
       'coupon_discount': coupon_discount,
       'cart_items_with_temp_amount': cart_items_with_temp_amount, # pass the zipped list to the template
       'variations': variations 
   })
