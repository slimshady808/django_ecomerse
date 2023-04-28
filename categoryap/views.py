from django.shortcuts import render
from productap.models import Product,Category,ProductVariation
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
#product listing  filter,search,sort
def cate_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    brands = Product.objects.values('brand').distinct()
    brands = [brand['brand'] for brand in brands]
    brands = list(set(brands))  # remove duplicates
    unique_colors = ProductVariation.objects.filter(type='color').values_list('variation_value', flat=True).distinct()

    paginator = Paginator(products, 4)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cate/category.html', {'categories': categories, 'products': page_obj, 'brands': brands,'unique_colors':unique_colors})

# category wise product listing


def category_item(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    # Set the number of items to display per page
    items_per_page = 3

    # Create a Paginator object
    paginator = Paginator(products, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page_obj = paginator.get_page(page_number)

    return render(request, 'cate/category_products.html', {'products': page_obj, 'category': category})




def filter_data(request):
    user=request.user
    
    categories = request.GET.getlist('category[]')
    colors = request.GET.getlist('color[]')
    brands = request.GET.getlist('brand[]')
    search_query = request.GET.get('q', '')
    allProducts = Product.objects.all().order_by('-id').distinct()

    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()

    if len(colors) > 0:
        allProducts = allProducts.filter(variations__variation_value__in=colors, variations__type='color').distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(brand__in=brands).distinct()

    if search_query:
        allProducts = allProducts.filter(name__icontains=search_query)

    # Get sort option
    sort_option = request.GET.get('sort', '')
    # Add sort option to queryset
    if sort_option == '1':
        allProducts = allProducts.order_by('-price')
    elif sort_option == '2':
        allProducts= allProducts.order_by('price')
    if request.user:
        t = render_to_string('ajax/product-list.html', {'data': allProducts,'user':user})
    else:

        t = render_to_string('ajax/product-list.html', {'data': allProducts})
    return JsonResponse({'data': t})
