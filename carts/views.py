from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import requests

from django.http import HttpResponse

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    
    if not cart:
        cart = request.session.create()
    
    return cart

def cart(request):
    total =0
    quantity =0
    cart_items=None

    try:
        if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user= request.user, is_active=True)

        else:
            cart  = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.all().filter(cart_id= cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product_id.price * cart_item.quantity)
            quantity += cart_item.quantity

    except ObjectDoesNotExist:
        pass
    
    tax = round((.02 * total),2)
    grand_total = total + tax
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html',context)

def add_cart(request, product_id):

    current_user = request.user
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation  = Variation.objects.get(product=product, variation_category__iexact = key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    # check if user is authenticated or not
    if current_user.is_authenticated:
        
        is_cart_item_exist = CartItem.objects.filter(product_id=product,user=current_user).exists()
        if is_cart_item_exist:

            cart_items = CartItem.objects.filter(product_id=product,user=current_user)

            # existing variation >> DB
            # product variation or current variation >> request
            # cart id >> DB
            existing_variation_list = []
            id = []

            for cart_item in cart_items:
                existing_variation = cart_item.variation.all()
                existing_variation_list.append(list(existing_variation))
                id.append(cart_item.id)

            if product_variation in existing_variation_list:
                # increment quantity 
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                cart_item = CartItem.objects.get(product_id=product, id=item_id)
                cart_item.quantity += 1
                cart_item.save()
            
            else:
                # create new ones
                cart_item = CartItem.objects.create(product_id=product, quantity = 1, user=current_user)
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation) 
                cart_item.save()        

        else:
            cart_item = CartItem.objects.create(product_id=product, quantity = 1, user=current_user)
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation) 
            cart_item.save()
    
    #if user isnot authenticated , use request session key to add new carts
    else:
        try:
            cart = Cart.objects.get(cart_id= _cart_id(request))
        
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id= _cart_id(request))

        cart.save()

        is_cart_item_exist = CartItem.objects.filter(product_id=product,cart_id=cart).exists()
        if is_cart_item_exist:

            cart_items = CartItem.objects.filter(product_id=product,cart_id=cart)

            # existing variation >> DB
            # product variation or current variation >> request
            # cart id >> DB
            existing_variation_list = []
            id = []

            for cart_item in cart_items:
                existing_variation = cart_item.variation.all()
                existing_variation_list.append(list(existing_variation))
                id.append(cart_item.id)
            print(id)

            if product_variation in existing_variation_list:
                # increment quantity 
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                cart_item = CartItem.objects.get(product_id=product, id=item_id)
                cart_item.quantity += 1
                cart_item.save()
            
            else:
                # create new ones
                cart_item = CartItem.objects.create(product_id=product, quantity = 1, cart_id=cart)
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation) 
                cart_item.save()        

        else:
            cart_item = CartItem.objects.create(product_id=product, quantity = 1, cart_id=cart)
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation) 
            cart_item.save()

    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product,id=product_id)
    current_user = request.user

    try:
        if current_user.is_authenticated:
            cart_items = CartItem.objects.get(product_id=product, user=current_user, id = cart_item_id)

        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            cart_items = CartItem.objects.get(product_id=product, cart_id=cart, id = cart_item_id)

    except:
        pass

    try:
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
        else:
            cart_items.delete()
    except:
        pass
    
    return redirect('cart')

def remove_cart_items(request, product_id,cart_item_id):
    product = get_object_or_404(Product,id=product_id)
    current_user = request.user

    try:
        if current_user.is_authenticated:
            cart_items = CartItem.objects.get(product_id=product, user=current_user, id = cart_item_id)
            cart_items.delete()

        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            cart_items = CartItem.objects.get(product_id=product, cart_id=cart, id = cart_item_id)
            cart_items.delete()

    except:
        pass
    
    return redirect('cart')

@login_required(login_url = 'login')
def checkout(request):
    total =0
    quantity =0
    cart_items=None

    try:
        if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user= request.user, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product_id.price * cart_item.quantity)
            quantity += cart_item.quantity

    except ObjectDoesNotExist:
        pass
    
    tax = round((.02 * total),2)
    grand_total = total + tax
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items' : cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/checkout.html', context)