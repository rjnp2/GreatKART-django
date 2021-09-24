from django.shortcuts import render, get_object_or_404, redirect
from category.models import Category
from .models import Product, ReviewRating, ProductGallery
from carts.models import Cart, CartItem
from carts.views import _cart_id
from .forms import ReviewRatingForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from orders.models import Order_Product

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

    orderproduct = False

    try:
        product_gallery = ProductGallery.objects.filter(product__id = single_product.id)

    except:
        product_gallery = None

    if request.user.is_authenticated:
        try:
            orderproduct = Order_Product.objects.filter(user=request.user, product_id=single_product.id).exists()
        except Order_Product.DoesNotExist:
            orderproduct = False

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context = {
        'single_product': single_product,
        'is_cart': is_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallery':product_gallery
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

def submit_review(request, product_id):
    print(product_id)

    url = request.META.get('HTTP_REFERER')    
    if request.method == 'POST':

        try:
            reviewrating = ReviewRating.objects.get(user__id = request.user.id, product = product_id)
            reviewratingform = ReviewRatingForm(request.POST, instance=reviewrating)
            reviewratingform.save()
            messages.success(request, 'Thank You!, your review has been updated')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            reviewratingform = ReviewRatingForm(request.POST)

            if reviewratingform.is_valid():
                reviewrating = ReviewRating()
                reviewrating.subject = reviewratingform.cleaned_data['subject']
                reviewrating.rating = reviewratingform.cleaned_data['rating']
                reviewrating.review = reviewratingform.cleaned_data['review']
                reviewrating.ip = request.META.get('REMOTE_ADDR')   
                reviewrating.product_id = product_id
                reviewrating.user_id =  request.user.id
                reviewrating.save()

                messages.success(request, 'Thank You!, your review has been submitted')
                return redirect(url)
            
            else:
                messages.error(request, 'Some Error in review form')
                return redirect(url)