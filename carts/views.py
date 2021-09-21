from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    
    return cart

def cart(request, total =0, quantity =0, cart_items=None):

    try:
        cart  = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart_id= cart, is_active=True)
        
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
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
    
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id= _cart_id(request))

    cart.save()

    try:
        cart_items = CartItem.objects.get(product_id=product, cart_id=cart)
        cart_items.quantity += 1
        cart_items.save()

    except CartItem.DoesNotExist:
        cart_items = CartItem.objects.create(product_id=product, quantity = 1, cart_id=cart)
        cart_items.save()

    return redirect('cart')

def remove_cart(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    cart = Cart.objects.get(cart_id= _cart_id(request))
    cart_items = CartItem.objects.get(product_id=product, cart_id=cart)

    if cart_items.quantity > 1:
        cart_items.quantity -= 1
        cart_items.save()
    else:
        cart_items.delete()
    
    return redirect('cart')

def remove_cart_items(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    cart = Cart.objects.get(cart_id= _cart_id(request))
    cart_items = CartItem.objects.get(product_id=product, cart_id=cart)

    cart_items.delete()
    
    return redirect('cart')