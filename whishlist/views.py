from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Whishlist
from productap.models import Product
from django.views.decorators.http import require_POST
from django.http import HttpResponseNotFound
# Create your views here.
def add_whishlist(request):
    pid=request.GET['product_id']
    product=Product.objects.get(pk=pid)
    data={}
    checkw=Whishlist.objects.filter(product=product,user=request.user).count()
    if checkw>0:
        data={
            'bool':False
        }
    else:
        wishlist=Whishlist.objects.create(
             product=product,
            user=request.user

        )
        data={
            'bool':True
        }
    return JsonResponse(data)

    # 

def view_whishlist(request):
    wish=Whishlist.objects.filter(user=request.user).order_by('-id')
    return render(request,'whishlist.html',{'wish':wish})


@require_POST
def delete_whishlist(request, product_id):
    try:
        # Get the whishlist object and check if it belongs to the current user
        whishlist = Whishlist.objects.get(product_id=product_id, user=request.user)
    except Whishlist.DoesNotExist:
        # Return a 404 response if the whishlist object does not exist or does not belong to the current user
        return HttpResponseNotFound()

    # Delete the whishlist object and redirect to the whishlist page
    whishlist.delete()
    return redirect('view_whishlist')
