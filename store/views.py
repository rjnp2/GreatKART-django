from django.shortcuts import render, get_object_or_404
from category.models import Category
from .models import Product
from carts.models import Cart, CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.
def store(request,category_slug=None):

    products = None
    categorys = None
    page_products = []
    products = []
    product_count = 0

    if category_slug:
        categorys = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category= categorys,is_available=True).order_by('id')
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        
    product_count = products.count()

    context = {
        'products': page_products,
        'product_count': product_count
    }

    return render(request, 'store/store.html',context)

def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug= category_slug, slug=product_slug)
        is_cart = CartItem.objects.filter(cart_id__cart_id = _cart_id(request),product_id = single_product).exists()

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'is_cart': is_cart
    }
    return render(request, 'store/product-detail.html',context)

def search(request):

    page_products = []
    products = []
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword)| Q(product_name__icontains=keyword) | Q(category__slug=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count
    }

    return render(request, 'store/store.html',context)
