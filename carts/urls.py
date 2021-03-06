from django.urls import path
from .views import cart, add_cart,remove_cart,remove_cart_items, checkout

urlpatterns = [
    path('', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', remove_cart, name='remove_cart'),
    path('remove_cart_items/<int:product_id>/<int:cart_item_id>/', remove_cart_items, name='remove_cart_items'),
    path('checkout/', checkout, name='checkout'),
]