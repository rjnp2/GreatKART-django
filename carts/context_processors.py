from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_counter = 0

    if 'admin' in request.path:
        return []
    
    else:
        try:
            cart  = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.all().filter(cart_id= cart)

            for cart_item in cart_items:
                cart_counter += cart_item.quantity
        
        except Cart.DoesNotExist:
            cart_counter = 0

    return dict(cart_counter = cart_counter)