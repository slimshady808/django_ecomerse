from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
#request.user.is_authenticated and 
def admin_login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_page')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('admin_login')
    else:
        return render(request, 'admin/admin_login.html')


def admin_page(request):
    return render(request,'admin/admin_panel.html')




# views.py
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from productap.models import Product, ProductVariation
from productap.forms import ProductForm, ProductVariationForm

def add_product(request):
    product_form = ProductForm(request.POST or None, request.FILES or None)
    ProductVariationFormSet = inlineformset_factory(Product, ProductVariation, form=ProductVariationForm, extra=1, can_delete=True)
    variation_formset = ProductVariationFormSet(request.POST or None, request.FILES or None, prefix='variations')

    if request.method == 'POST':
        if product_form.is_valid() and variation_formset.is_valid():
            product = product_form.save(commit=False)
            variation_instances = variation_formset.save(commit=False)

            if not variation_instances:
                product_form.add_error(None, 'Please add at least one product variation.')
                return render(request, 'admin/add_product.html', {'product_form': product_form, 'variation_formset': variation_formset})

            product.save()
            for variation in variation_instances:
                variation.product = product
                variation.save()

            return redirect('product_detail', slug=product.slug)
    
    context = {
        'product_form': product_form,
        'variation_formset': variation_formset,
    }
    return render(request, 'admin/add_product.html', context)
